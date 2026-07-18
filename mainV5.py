import logging
from core import logging_configuration
from core import builtin_commands
import custom_commands
#from tools.tts import voice
#from tools.stt.recognizer import load_model
#from tools.stt.recognizer import create_mic
#from tools.stt.recognizer import wake_word_detection
#from tools.stt.recognizer import get_user_command
from tools.spotify import spotipy_commands
from tools.model import model
from tools.toolbox import toolboxv2
from session import session
from core.credential_checker import check_all_credentials

#/logging configuration

logging_configuration.configure_logging()
main_logger = logging.getLogger("main")
#====

#/flags configuration
#mute_joseh = True
#speech_wait_time = 5
command_via_speech = False
#wake_word = "michael"
SKIP_NOUN_WARNING = True
DEBUG_MODE = False
if not DEBUG_MODE: logging_configuration.disable_debug_mode()
if SKIP_NOUN_WARNING: model.enable_ignore_type_warning_flag()
flags = {"command_via_speech": command_via_speech, "skip_noun_warning": SKIP_NOUN_WARNING, "debug_mode": DEBUG_MODE}
for name, value in flags.items():
    active_flags = []
    if value:
        active_flags.append(name)

#/start configuration
#//stt
#stt_model = load_model('/home/rodrigo/Joseh/tools/stt/vosk-model-en-us-0.22')
#mic_object = create_mic()
#//initial credential check
credentials_present = check_all_credentials()
#//tts
#voice.tts_configuration()
#if mute_joseh: voice.mute_joseh()
#//spotify
if not "SP" in credentials_present:
    main_logger.warning("Spotify credentials are not present! To create type 'direct command mode' into Joseh and then type '3'.")
else: 
    spotipy_commands.spotipy_configuration()
#//system credentials check
if not "SY" in credentials_present:
    main_logger.warning("System credentials were not set. To set please type 'direct command mode', then '1'.")
#//initiate the OS variable
main_logger.info(f"Detected OS: {toolboxv2.detect_os()}")
#//nlp
model.init_models()
#//flatpak module
toolboxv2.get_installed_flatpak_programs()

#/main loop
main_logger.info("Joseh started")
session_finished = False
for flag in active_flags:
    main_logger.warning(f"Active flag: {flag}")
while not session_finished:
    session_finished = session(active_flags)
