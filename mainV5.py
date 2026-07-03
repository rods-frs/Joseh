import logging
from core.logging_configuration import configure_logging
from core import builtin_commands
#from tools.tts import voice
#from tools.stt.recognizer import load_model
#from tools.stt.recognizer import create_mic
#from tools.stt.recognizer import wake_word_detection
#from tools.stt.recognizer import get_user_command
from tools.spotify import spotipy_commands
from tools.model import model
from tools.toolbox import toolboxv2
from core.error_handler import JosehError, NLPError, InvalidCommand, NoNounDetected, ToolboxError, SpotifyError, SpotifyTrackNotFound

#/logging configuration

configure_logging()
main_logger = logging.getLogger("main")
#====

#/flags configuration
#mute_joseh = True
#speech_wait_time = 5
command_via_speech = False
#wake_word = "michael"
SKIP_NOUN_WARNING = True
if SKIP_NOUN_WARNING:
    model.enable_ignore_type_warning_flag()

#/start configuration
#//stt
#stt_model = load_model('/home/rodrigo/Joseh/tools/stt/vosk-model-en-us-0.22')
#mic_object = create_mic()

#//tts
#voice.tts_configuration()
#if mute_joseh: voice.mute_joseh()

#//spotify
spotify_credentials_present = spotipy_commands.check_spotify_credential()
if not spotify_credentials_present:
    main_logger.warning("Spotify credentials are not present! To create type 'direct command mode' into Joseh and then type '2'.")
else: 
    spotipy_commands.spotipy_configuration()

#//nlp
model.init_models()

#//system credentials check
system_credentials_present = builtin_commands.check_system_credentials()
if not system_credentials_present:
    main_logger.warning("System credentials were not set. To set please type 'direct command mode', then '1'.")

#//user commands
SPOTIFY_COMMANDS = ['resume', 'pause', 'next', 'previous', 'get_music', 'play_music']
TOOLBOX_COMMANDS = ['update', 'date', 'open_program']

#custom commands configuration
def custom_command_mode():
    #custom commands codes:
    #001 - delete user password
    usr_command = int(input(">> "))
    if usr_command == 1:
        try:
            toolboxv2.delete_user_password()
        except JosehError as e:
            pass

#/main loop
main_logger.debug("Joseh started")
session_finished = False
while session_finished == False:
    print("=/"*10)
    main_logger.info("New session started")
    sp_detected_commands =[]
    tb_detected_commands = []
    valid_command = False
    #//speech commands
    if command_via_speech:
        pass
        #wake_word_heard = wake_word_detection(stt_model, mic_object, wake_word)
        #print(wake_word_heard)
    else:
        while not valid_command:
            user_command = str(input("What`s your command?\n>> "))
            if user_command.lower() == "exit":
                main_logger.info("User finished the session")
                session_finished = True
                break
            elif user_command.lower() == "custom command mode":
                custom_command_mode()
                break
            elif user_command.lower() == "direct command mode":
                builtin_commands.direct_command_mode()
                break
            else:
                try:
                    detected_commands, special_clauses = model.detect_intent(user_command)
                    main_logger.debug(f"Command(s) validated. Detected commands: {', '.join(detected_commands)}")
                    valid_command = True
                except InvalidCommand as e:
                    print(f"The command '{user_command}' has not being recognized. Please try different words of a different command.")
                except JosehError as e:
                    print(f"Something went wrong, please try again. Specific error: {e}")

        for command in detected_commands:
            if command in SPOTIFY_COMMANDS:
                if spotify_credentials_present:
                        sp_detected_commands.append(command)
                else: main_logger.warning(f"Spotify credentials were not set. Ignoring command {command}")
            else:
                if not system_credentials_present and command == "update": main_logger.error(f"System credentials were not set. Ignoring command {command}")
                else:
                    tb_detected_commands.append(command)
        try:
            if sp_detected_commands:
                spotipy_commands.spotify_command_list()
                spotipy_commands.execute_spotify_commands(sp_detected_commands, special_clauses if special_clauses else [], ner_function=model.detect_noun_name)
            if tb_detected_commands:
                pass
        except JosehError as e:
            print(f"Something went wrong. Specific error: {e}")
        main_logger.info("Session finished.")

    



    