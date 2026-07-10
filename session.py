import logging
import custom_commands
from core import builtin_commands
from tools.spotify import spotipy_commands
from tools.model import model
from tools.toolbox import toolboxv2
from core.error_handler import JosehError, InvalidCommand

session_logger = logging.getLogger("SESSION")
spotify_credentials_present = spotipy_commands.check_spotify_credential()
system_credentials_present = builtin_commands.check_system_credentials()
sp_detected_commands = []
tb_detected_commands = []
special_commands = [""]

def execute_general_command(detected_commands, special_clauses=[]):
    SPOTIFY_COMMANDS = ['resume', 'pause', 'next', 'previous', 'get_music', 'play_music']
    for command in detected_commands:
        if command in SPOTIFY_COMMANDS:
            if spotify_credentials_present:
                    sp_detected_commands.append(command)
            else: session_logger.warning(f"Spotify credentials were not set. Ignoring command {command}")
        else:
            if not system_credentials_present and command == "update": session_logger.error(f"System credentials were not set. Ignoring command {command}")
            else:
                tb_detected_commands.append(command)
    try:
        if sp_detected_commands:
            spotipy_commands.spotify_command_list()
            spotipy_commands.execute_spotify_commands(sp_detected_commands, special_clauses if special_clauses else [], ner_function=model.detect_noun_name)
        if tb_detected_commands:
            toolboxv2.execute_toolbox_commands(tb_detected_commands, special_clauses if special_clauses else [], ner_function=model.detect_noun_name)
    except JosehError as e:
        print(f"Something went wrong. Specific error: {e}")

def session(active_flags):
    print("=/"*10)
    session_logger.info("New session started")
    sp_detected_commands =[]
    tb_detected_commands = []
    valid_command = False
    special_command = False
    session_finished = False
    #//speech commands
    if "command_via_speech" in active_flags:
        pass
        #wake_word_heard = wake_word_detection(stt_model, mic_object, wake_word)
        #print(wake_word_heard)
    else:
        while not valid_command:
            user_command = str(input("What`s your command?\n>> "))
            if user_command.lower() == "exit":
                session_logger.info("User finished the session")
                session_finished = True
                special_command = True
                valid_command = True
            elif user_command.lower() == "custom command mode":
                custom_commands.custom_command_executer()
                valid_command = True
                special_command = True
                valid_command = True
            elif user_command.lower() == "direct command mode":
                builtin_commands.direct_command_mode(spotipy_commands.create_credential)
                valid_command = True
                special_command =  True
                valid_command = True
            else:
                try:
                    detected_commands, special_clauses = model.detect_intent(user_command)
                    session_logger.debug(f"Command(s) validated. Detected commands: {', '.join(detected_commands)}")
                    valid_command = True
                except InvalidCommand as e:
                    print(f"The command '{user_command}' has not being recognized. Please try different words of a different command.")
                except JosehError as e:
                    print(f"Something went wrong, please try again. Specific error: {e}")

        if not special_command:
            execute_general_command(detected_commands, special_clauses)
        session_logger.info("Session finished.")
        return session_finished