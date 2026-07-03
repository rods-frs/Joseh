import re
import logging
import subprocess
import platform
import distro
import keyring
from core.error_handler import ToolboxError
from datetime import datetime

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

def get_date():
    toolbox_logger.debug("Getting date")
    print(f"Today is: {datetime.today().strftime(r'"%A, %B %dst %Y"')}")

