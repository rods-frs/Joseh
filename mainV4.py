#importing libraries
import joseh_toolbox as jt
import speech_recognition as sr
from time import sleep
import random
import logging

#main logger
main_logger = logging.getLogger("main")
main_logger.setLevel(logging.INFO)
main_formatter = logging.Formatter("[MAIN] %(message)s")
main_handler = logging.StreamHandler()
main_handler.setFormatter(main_formatter) 
main_logger.addHandler(main_handler)  

#toolbox logger
toolbox_logger = logging.getLogger("toolbox")
toolbox_logger.setLevel(logging.DEBUG)
toolbox_logger.addHandler(logging.FileHandler("toolbox.log"))
toolbox_formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s",datefmt="%Y-%m-%d %H:%M:%S")
toolbox_handler = logging.StreamHandler()
toolbox_handler.setFormatter(toolbox_formatter)
toolbox_logger.addHandler(toolbox_handler)
toolbox_logger.propagate = False

#flags
COMMAND_VIA_SPEECH = True
SKIP_SIMPLE_COMMAND_VERIFICATION = True
JOSEH_MUTED = False
if JOSEH_MUTED: jt.mute_joseh()
flags = {"command_via_speech": COMMAND_VIA_SPEECH, "skip_simple_command_verification": SKIP_SIMPLE_COMMAND_VERIFICATION, "joseh_muted": JOSEH_MUTED}

#initial setup
r= jt.setup()

#variables pre-loading
program_name = ""
music_name = ""
simple_command = ""
wake = False
session_finished = False

#global variables
SPEECH_WAIT_TIME = 5
commands_map = {
    "resume": lambda:jt.resume_music(),
    "pause": lambda:jt.pause_music(),
    "next": lambda:jt.next_track(),
    "previous": lambda:jt.previous_track(),
    "update": lambda:jt.update_system(),
    "date": lambda:jt.get_date(),
    "get_music": lambda:jt.get_music(),
    "open_program": lambda:jt.open_program(program_name),
    "play_music": lambda:jt.play_music(jt.get_music_id(music_name))
}
special_intetions = ["open_program", "play_music"]
introduction_phrases = [
    "Hello! I`m Joseh! How can I help?", 
    "Hey! my name is Joseh, at your orders!", 
    "Welcome! I`m Joseh! How can I help you today?"
    ]

#main code
if __name__ == "__main__":
        #main loop
            logging.info("Joseh started")
            for flag, status in flags.items():
                if status:
                    logging.warning(f"Active flag: {flag}")
            grettings_phrase = random.choice(introduction_phrases)
            jt.talk_and_print(grettings_phrase)
            while not session_finished:
                wake = False                
                logging.info("Starting new session")
                if COMMAND_VIA_SPEECH:
                    logging.debug("COMMAND_VIA_SPEECH detected. Speech commands enabled")
                    while True:
                        print("="*10)
                        wake_word_detected = jt.wait_for_wake_word("Marco")
                        if wake_word_detected and wake_word_detected != "CANCEL":
                            logging.debug("Wake word returned True.")
                            while True or usr_input.lower() != "cancel":
                                try:
                                    jt.talk_and_print("Wake word detected! Whats your command?")
                                    usr_input = jt.hear_user(SPEECH_WAIT_TIME)
                                    if usr_input:
                                        logging.debug("usr_input didnt returned None.")
                                        break
                                    else: 
                                        raise TypeError("usr_input returned None.")
                                except Exception as e:
                                    jt.talk_and_print("Sorry, I didn`t understood what you said, please try again")
                                    logging.error(f"Error while understanding the user speech: {e} | User speech: {usr_input}")
                            break
                        elif wake_word_detected == "CANCEL":
                            logging.info("User canceled hearing. Exiting...")
                            session_finished = True
                        else: logging.warning("Wake word detected variable returned False. This should not happen. Please check.")
                else:
                    print("="*10)
                    jt.talk_and_print("Whats your command?")
                    usr_input = str(input(">> "))
                    logging.debug(f"User input: {usr_input}")
                if usr_input:
                    logging.debug("User input is not blank. Continuing")
                    if usr_input == "exit":
                        jt.talk_and_print("Okay, Goodbye")
                        print("Session finilized by the user")
                        logging.info("Session finished by the user")
                        session_finished = True

                    if not SKIP_SIMPLE_COMMAND_VERIFICATION:
                        simple_command, command_list = jt.check_simple_command(commands_map, usr_input)
                        if simple_command:
                            logging.debug("Simple command detected! Executing...")
                            jt.execute_spotify_commands(command_list, commands_map)

                    if not simple_command or SKIP_SIMPLE_COMMAND_VERIFICATION:
                        logging.debug("simple_command returned None or SKIP_SIMPLE_COMMAND_VERIFICATION is active. Passing user command to Joseh...")
                        intents = jt.intent_recognition(usr_input)
                        if intents:
                            for intention in intents:
                                action = commands_map.get(intention)
                                if action:
                                    if intention in special_intetions:
                                        logging.debug("Special intention recognized!")
                                        if intention == "open_program":
                                            program_name = jt.get_program_name(usr_input)
                                            logging.debug(f"Program name recognized: {program_name}")
                                        elif intention == "play_music":
                                            music_name = jt.get_music_name(usr_input)
                                            logging.debug(f"Music name recognized: {music_name}")
                                    jt.talk_and_print(f"Executing command: {intention}")
                                    print("="*10)
                                    sleep(1.5)
                                    action()
                        else:
                            logging.error("No intents were returned from the model.")
                            jt.talk_and_print("Sorry, i couldnt recognize your intention. Please try using other words or a simples phrase.")

                else: logging.error("User input is blank but it should not be at this part of the code. Please check")
                logging.info("Session finished.")

            
