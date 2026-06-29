import re
import logging
import subprocess
import platform
import distro
import keyring
from core.error_handler import ToolboxError

toolbox_logger = logging.getLogger("TB")

def detect_os():
    global OS
    toolbox_logger.debug("Detecting user OS")
    plataform = platform.system()
    if plataform == "Linux":
        OS = distro.name()
    else:
        OS = "windows"
    toolbox_logger.debug(f"Recognized OS: {OS}")
    return OS

def check_and_create_system_credentials():
    toolbox_logger.debug("Checking for user password in system keyring...")
    try:
        global USER_PASSWORD
        USER_PASSWORD = keyring.get_password("joseh", "system_password")
        if not USER_PASSWORD:
            toolbox_logger.debug("User password is not in the keyring.")
            while True:
                user_response = str(input("Could you please write your password? (y/n) >> "))
                if user_response.lower() == "y": 
                    USER_PASSWORD = str(input("Please type your password: "))
                    keyring.set_password("joseh", "system_password", USER_PASSWORD)
                    toolbox_logger.debug("Password was sent to the keyring")
                    break
                elif user_response == "n":
                    toolbox_logger.warning("User opted to not give the system password.")
                    break
                else: toolbox_logger.error(f"The input {user_response} is not valid, please try again.")
        else: toolbox_logger.debug("User password was found in the keyring.")
    except Exception as e:
        raise ToolboxError(f"Failed to process user password from the keyring: {e}")

def delete_user_password():
    toolbox_logger.info("Starting user password deletion from the keyring")
    try:
        while True:
            usr_response = str(input("Do you really want to delete your password from the keyring? (y/n) >> "))
            if usr_response.lower() == "y":
                keyring.delete_password("joseh", "system_password")
                toolbox_logger.info("Password deleted from the keyring.")
                break
            elif usr_response.lower() == "n":
                toolbox_logger.info("Aborting deletion")
                break
            else:
                toolbox_logger.error(f"The input {usr_response} is not valid. Please try again.")
    except Exception as e:
        raise ToolboxError(f"Failed to delete the user password from the keyring: {e}")

def update_system():
    toolbox_logger.debug("Starting system update module")
    detect_os()
    if "Fedora" in OS:
        command = ["sudo", "-S", "dnf", "upgrade", "-y"]
    elif "Ubuntu" in OS:
        command = ["sudo", "-S", "sh", "-c", "apt-get update && apt-get upgrade -y"]
    elif "Arch" in OS:
        command = ["sudo", "-S", "pacman", "-Syu", "--noconfirm"]
    else:
        toolbox_logger.error("OS not supported for this command.")
    try:
        subprocess.run(command,input=f"{USER_PASSWORD}\n",text=True,capture_output=True,check=True)
        toolbox_logger.info("System updated!")
    except Exception as e:
        raise ToolboxError(f"Failed to update the system: {e}")

