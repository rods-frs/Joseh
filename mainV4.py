#importing libraries
import joseh_toolbox as jt
import speech_recognition as sr
from time import sleep
import random

#initial setup
logging, sp, base_model, cat_model, ner_model, OS, r, engine = jt.setup()

#flags
COMMAND_VIA_SPEECH = False
SKIP_SIMPLE_COMMAND_VERIFICATION = True
JOSEH_MUTED = True
flags = {"command_via_speech": COMMAND_VIA_SPEECH, "skip_simple_command_verification": SKIP_SIMPLE_COMMAND_VERIFICATION, "joseh_muted": JOSEH_MUTED}

#variables pre-loading
program_name = ""
music_name = ""
simple_command = ""

#global variables
SYSTEM_PASSWORD = "Herocraft"
SPEECH_WAIT_TIME = 10
commands_map = {
    "resume": lambda:jt.resume_music(engine, sp),
    "pause": lambda:jt.pause_music(engine, sp),
    "next": lambda:jt.next_track(engine, sp),
    "previous": lambda:jt.previous_track(engine, sp),
    "update": lambda:jt.update_system(OS, SYSTEM_PASSWORD, engine),
    "date": lambda:jt.get_date(engine),
    "get_music": lambda:jt.get_music(engine, sp),
    "open_program": lambda:jt.open_program(program_name),
    "play_music": lambda:jt.play_music(jt.get_music_id(music_name, sp), sp, engine)
}
special_intetions = ["open_program", "play_music"]
introduction_phrases = ["Hello! I`m Joseh! How can I help?", "Hey! my name is Joseh, at your orders!", "Welcome! I`m Joseh! How can I help you today?"]

#main code
if __name__ == "__main__":
        logging.info("Program started")
        for flag, status in flags.items():
            if status:
                logging.warning(f"Active flag: {flag}")
        if JOSEH_MUTED: jt.mute_joseh()
        grettings_phrase = random.choice(introduction_phrases)
        jt.talk_and_print(engine, grettings_phrase)

        #main loop
        while True:
            if COMMAND_VIA_SPEECH:
                while True:
                    print("="*10)
                    logging.debug("COMMAND_VIA_SPEECH detected. Speech commands enabled")
                    jt.talk(engine, "Press enter to start talking")
                    input("Press ENTER to speak")
                    try:
                        logging.debug("Trying to hear user")
                        with sr.Microphone() as source:
                            jt.talk_and_print(engine, "Now lissening")
                            r.adjust_for_ambient_noise(source, duration=1)
                            audio = r.listen(source, phrase_time_limit=SPEECH_WAIT_TIME)
                        usr_input = r.recognize_google(audio, language="en_US")
                        logging.debug(f"Recognized speech: {usr_input}")
                        break
                    except Exception as e:
                        jt.talk_and_print(engine, "Sorry, I didn`t understood what you said, please try again")
                        logging.error(f"Error while understanding the user speech: {e} | User speech: {usr_input}")
            
            else:
                 print("="*10)
                 jt.talk_and_print(engine, "Whats your command?")
                 usr_input = str(input(">> "))
                 logging.debug(f"User input: {usr_input}")
            
            if usr_input == "exit":
                jt.talk_and_print(engine, "Okay, Goodbye")
                print("Session finilized by the user")
                logging.info("Session finished by the user")
                break
            
            if not SKIP_SIMPLE_COMMAND_VERIFICATION:
                simple_command, command_list = jt.check_simple_command(commands_map, base_model, usr_input)
                if simple_command:
                    logging.debug("Simple command detected! Executing...")
                    jt.execute_spotify_commands(command_list, commands_map)

            else: logging.warning("Skip simple command verification parameter is active. Skipping verification...")

            if not simple_command or SKIP_SIMPLE_COMMAND_VERIFICATION:
                logging.debug("simple_command returned None or SKIP_SIMPLE_COMMAND_VERIFICATION is active. Passing user command to Joseh...")
                intents = jt.intent_recognition(usr_input, cat_model)
                if intents:
                    for intention in intents:
                        action = commands_map.get(intention)
                        if action:
                            if intention in special_intetions:
                                logging.debug("Special intention recognized!")
                                if intention == "open_program":
                                    program_name = jt.get_program_name(usr_input, ner_model)
                                    logging.debug(f"Program name recognized: {program_name}")
                                elif intention == "play_music":
                                    music_name = jt.get_music_name(usr_input, ner_model)
                                    logging.debug(f"Music name recognized: {music_name}")
                            jt.talk_and_print(engine, f"Executing command: {intention}")
                            print("="*10)
                            sleep(1.5)
                            action()
                else:
                    logging.error("No intents were returned from the model.")
                    jt.talk_and_print(engine, "Sorry, i couldnt recognize your intention. Please try using other words or a simples phrase.")

            
