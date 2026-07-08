import logging
import keyring
from dotenv import set_key
from core.error_handler import BuiltInCommandsError, BICommandNotFound
from tools.toolbox import toolboxv2

bic_logger = logging.getLogger("BIC")

def direct_command_mode(spotify_credentials_creation):
    bic_logger.info("Entering direct command mode. Type 'exit' to leave")
    valid_command = False
    while not valid_command:
        user_command = int(input("Type the number code of your command: "))
        for key, value in commands_map.items():
            if user_command == key: 
                if key == 3:
                    value(spotify_credentials_creation)
                else:
                    value()
                valid_command = True
        if not valid_command: BuiltInCommandsError("The code {user_command} is not a valid code. Please try again or type 'exit'.")

def check_system_credentials():
    bic_logger.debug("Checking keyring for system password")
    try:
        user_password = keyring.get_password("joseh", "system_password")
        if user_password:
            bic_logger.debug(f"System password found: {"*"*len(user_password)}")
            return user_password
        else:
            bic_logger.debug("System password was not found in the keyring")
            return False
    except Exception as e:
        BuiltInCommandsError(f"Failed to check for the system credentials: {e}")

def create_system_credentials():
    bic_logger.info("Starting creation of system credentials")
    try:
        while True:
            user_password = str(input("Please type your password: "))
            user_response = str(input(f"It the password {user_password} right? (y/n): "))
            if user_response == "y":
                try:
                    keyring.set_password("joseh", "system_password", user_password)
                    bic_logger.info("Password saved to the keyring!")
                    break
                except Exception as e:
                    BuiltInCommandsError(f"Failed to set the user password into keyring: {e}")
            elif user_response == "n":
                pass
            else:
                bic_logger.error(f"The response '{user_response} is not valid. Please try again.'")
    except Exception as e:
        BuiltInCommandsError(f"Failed to create system credentials: {e}")

def delete_user_password():
    bic_logger.info("Starting user password deletion from the keyring")
    try:
        while True:
            usr_response = str(input("Do you really want to delete your password from the keyring? (y/n) >> "))
            if usr_response.lower() == "y":
                keyring.delete_password("joseh", "system_password")
                bic_logger.info("Password deleted from the keyring.")
                break
            elif usr_response.lower() == "n":
                bic_logger.info("Aborting deletion")
                break
            else:
                bic_logger.error(f"The input {usr_response} is not valid. Please try again.")
    except Exception as e:
        raise BuiltInCommandsError(f"Failed to delete the user password from the keyring: {e}")

def create_spotify_credentials(spotify_function):
    spotify_function()

def execute_specific_function():
    toolboxv2.open_program("steam")

commands_map = {1: create_system_credentials, 2: delete_user_password, 3: create_spotify_credentials, 4:execute_specific_function}