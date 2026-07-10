import logging
import keyring
from dotenv import set_key
from core.error_handler import BuiltInCommandsError, BICommandNotFound
from tools.toolbox import toolboxv2
from unittest.mock import patch, MagicMock

bic_logger = logging.getLogger("BIC")

def direct_command_mode(spotify_credentials_creation):
    bic_logger.info("Entering direct command mode. Type '0' to leave")
    valid_command = False
    while not valid_command:
        user_command = int(input("Type the number code of your command: "))
        if user_command == 0: break
        for key, value in commands_map.items():
            if user_command == key: 
                if key == 3:
                    value(spotify_credentials_creation)
                else:
                    value()
                valid_command = True
        if not valid_command: BuiltInCommandsError("The code {user_command} is not a valid code. Please try again or type '0' to exit.")

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
    PACMAN_OUTPUT = (
    ":: Synchronizing package databases...\n"
    " core                  150.0 KiB\n"
    " extra                   8.0 MiB\n"
    ":: Starting full system upgrade...\n"
    "resolving dependencies...\n"
    "looking for conflicting packages...\n"
    "\n"
    "Packages (3) python-3.12.3-1  git-2.45.0-1  curl-8.7.1-1\n"
    "\n"
    "Total Installed Size:  45.23 MiB\n"
    "Net Upgrade Size:       0.12 MiB\n"
    "\n"
    ":: Proceed with installation? [Y/n]\n"
    ":: Processing package changes...\n"
    "upgrading python (3.11.8-1 -> 3.12.3-1)\n"
    "upgrading git (2.44.0-1 -> 2.45.0-1)\n"
    "upgrading curl (8.6.0-1 -> 8.7.1-1)\n"
    ":: Running post-transaction hooks...\n"
    "Update finished.\n"
)
    fake_result = MagicMock()
    fake_result.return_value = 0
    fake_result.stdout = PACMAN_OUTPUT
    fake_result.stderr = ""
    with patch("subprocess.run", return_value=fake_result):
        toolboxv2.update_system()

commands_map = {1: create_system_credentials, 2: delete_user_password, 3: create_spotify_credentials, 4:execute_specific_function}