#importing toolbox
import joseh_toolbox as jt
import speech_recognition as sr
from time import sleep

#initial setup
logging, sp, base_model, cat_model, ner_model, OS, r, engine = jt.setup()

#parameters
COMMAND_VIA_SPEECH = False
SYSTEM_PASSWORD = "herocraft"
SPEECH_WAIT_TIME = 10

#variables pre-loading
program_name = ""
music_name = ""

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

if __name__ == "__main__":
        logging.info("Program started")
        jt.talk_and_print(engine, "Hello, my name is Joseh, at your orders!")
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
                 logging.debug("Speech commands are disabled")
                 jt.talk_and_print(engine, "Whats your command?")
                 usr_input = str(input(">> "))
                 logging.debug(f"User input: {usr_input}")
            
            if usr_input == "exit":
                jt.talk_and_print(engine, "Okay, Goodbye")
                print("Session finilized by the user")
                logging.info("Session finished by the user")
                break
            
            simple_command, command_list = jt.check_simple_command(commands_map, base_model, usr_input)
            if simple_command:
                logging.debug("Simple command detected! Executing...")
                jt.execute_spotify_commands(command_list, commands_map)

            else:
                logging.debug("Complex command detected! Passing input to Joseh NLP model...")
                intents = jt.intent_recognition(usr_input, cat_model)
                for intention in intents:
                    action = commands_map.get(intention)
                    if action:
                        if intention == "open_program":
                            logging.debug("Program intent recognized")
                            program_name = jt.get_program_name(usr_input, ner_model)
                            logging.debug(f"Program name recognized: {program_name}")
                        elif intention == "play_music":
                            logging.debug("play music intent recognized")
                            music_name = jt.get_music_name(usr_input, ner_model)
                            logging.debug(f"Music name recognized: {music_name}")
                        jt.talk_and_print(engine, f"Executing command: {intention}")
                        print("="*10)
                        sleep(1.5)
                        action()

            
