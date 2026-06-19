#importing libraries
import joseh_toolbox as jt
import speech_recognition as sr
from time import sleep
import random

#flags
COMMAND_VIA_SPEECH = True
SKIP_SIMPLE_COMMAND_VERIFICATION = True
JOSEH_MUTED = False
if JOSEH_MUTED: jt.mute_joseh()
flags = {"command_via_speech": COMMAND_VIA_SPEECH, "skip_simple_command_verification": SKIP_SIMPLE_COMMAND_VERIFICATION, "joseh_muted": JOSEH_MUTED}

#initial setup
logging, r= jt.setup()

#variables pre-loading
program_name = ""
music_name = ""
simple_command = ""
wake = False

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

            while True:
                wake = False                
                logging.info("Starting new session")
                if COMMAND_VIA_SPEECH:
                    while True:
                        print("="*10)
                        logging.debug("COMMAND_VIA_SPEECH detected. Speech commands enabled")
                        logging.info("Waiting for wake word")
                        while not wake:
                            logging.info("Hearing user")
                            try:
                                with sr.Microphone() as source:
                                    r.adjust_for_ambient_noise(source, duration=1)
                                    audio = r.listen(source, phrase_time_limit=SPEECH_WAIT_TIME)
                                usr_input = r.recognize_google(audio, language="en_US")
                                logging.debug(f"Recognized phrase: {usr_input}")
                                if "Marco" in usr_input:
                                    logging.info("Wake word detected!")
                                    wake = True
                                else:
                                    continue
                            except Exception as e:
                                logging.error(f"Failed to hear the user: {e}")
                        try:
                            with sr.Microphone() as source:
                                jt.talk_and_print("Hello! Now lissening")
                                r.adjust_for_ambient_noise(source, duration=1)
                                audio = r.listen(source, phrase_time_limit=SPEECH_WAIT_TIME)
                            usr_input = r.recognize_google(audio, language="en_US")
                            logging.debug(f"Recognized speech: {usr_input}")
                            break
                        except Exception as e:
                            jt.talk_and_print("Sorry, I didn`t understood what you said, please try again")
                            logging.error(f"Error while understanding the user speech: {e} | User speech: {usr_input}")
                
                else:
                    print("="*10)
                    jt.talk_and_print("Whats your command?")
                    usr_input = str(input(">> "))
                    logging.debug(f"User input: {usr_input}")
                
                if usr_input == "exit":
                    jt.talk_and_print("Okay, Goodbye")
                    print("Session finilized by the user")
                    logging.info("Session finished by the user")
                    break

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
                logging.info("Session finished.")

            
