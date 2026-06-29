import logging
from core.logging_configuration import configure_logging
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
credentials_present = spotipy_commands.check_credential()
if not credentials_present:
    credentials_present = spotipy_commands.create_credential() #returns true if the credentials were created succesfully
    if credentials_present: spotipy_commands.spotipy_configuration()
else: spotipy_commands.spotipy_configuration()

#//nlp
model.init_models()

#//user commands
SPOTIFY_COMMANDS = ['resume', 'pause', 'next', 'previous', 'get_music', 'play_music']
TOOLBOX_COMMANDS = ['update', 'date', 'open_program']

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
                sp_detected_commands.append(command)
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

    



    