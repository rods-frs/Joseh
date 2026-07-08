import re
import logging
import subprocess
import platform
import distro
import keyring
from core.error_handler import ToolboxError, FlatpakModuleError, ProgramNotFound
from datetime import datetime
import shutil

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
    _USER_PASSWORD = keyring.get_password("joseh", "system_password")
    if "Fedora" in OS:
        command = ["sudo", "-S", "dnf", "upgrade", "-y"]
    elif "Ubuntu" in OS:
        command = ["sudo", "-S", "sh", "-c", "apt-get update && apt-get upgrade -y"]
    elif "Arch" in OS:
        command = ["sudo", "-S", "pacman", "-Syu", "--noconfirm"]
    else:
        toolbox_logger.error("OS not supported for this command.")
        return
    try:
        toolbox_logger.debug("Executing update command.")
        result = subprocess.run(command,input=f"{_USER_PASSWORD}\n",text=True,capture_output=True,check=True)
        for line in result.stdout.splitlines():
            if "nothing to do" in line.lower():
                print("System is already updated")
            elif "upgrad " in line:
                print(line)
    except Exception as e:
        toolbox_logger.error(f"stderr: {getattr(e, 'stderr', 'N/A')}")
        raise ToolboxError(f"Failed to update the system: {e}")

def get_date():
    toolbox_logger.debug("Getting date")
    print(f"Today is: {datetime.today().strftime(r'"%A, %B %dst %Y"')}")

def get_installed_flatpak_programs():
    name_command = ["flatpak", "list", "--app","--columns=application"]
    try:
        toolbox_logger.debug("Getting the installed flatpak programs")
        global installed_flatpaks
        installed_flatpaks = subprocess.run(name_command,text=True,capture_output=True,check=True)
    except Exception as e:
        raise FlatpakModuleError(f"stderr: {getattr(e, 'stderr', 'N/A')}")

def start_flatpak_program(program):
    try:
        #try to find the program in the installed program list
        program_found = False
        toolbox_logger.debug(f"Trying to find a Flatpak by the name {program}")
        for line in installed_flatpaks.stdout.splitlines():
            if program in line.lower():
                toolbox_logger.debug("Program named is installed!")
                program_found = True
                print(line)
                execution_command = ["flatpak", "run", line]
                try:
                    toolbox_logger.debug(f"Trying to execute the program by the ID {line}")
                    subprocess.Popen(execution_command,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,start_new_session=True)
                except Exception as e:
                    raise FlatpakModuleError(f"stderr: {getattr(e, 'stderr', 'N/A')}")
        if program_found == False:
            raise ProgramNotFound(f"There was no Flatpak by the name {program}")
    except ProgramNotFound:
        raise
    except Exception as e:
        raise FlatpakModuleError(f"Something went wrong: {e}")

def start_normal_program(program):
    try:
        toolbox_logger.debug(f"Trying to find the program {program}")
        program_path = shutil.which(program)
        if not program_path:
            raise ProgramNotFound(f"The program {program} was not found in /bin and others.")
        else:
            toolbox_logger.debug("Program found! Executing...")
            subprocess.Popen(program_path,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,start_new_session=True)
            toolbox_logger.info(f"Program {program} executed!")
    except Exception as e:
        raise ToolboxError(f"Something went wrong here: {e}")

def open_program(ner_function, special_clauses, special_clauses_index):

    clause = special_clauses[int(special_clauses_index)]
    program = str(ner_function(clause, "program"))
    program = program.lower()
    if program:
        toolbox_logger.info(f"Trying to open the program {program}")
        try:
            start_flatpak_program(program)
        except ProgramNotFound:
            try:
                start_normal_program(program)
            except ProgramNotFound:
                raise
            except ToolboxError:
                raise
        except FlatpakModuleError:
            raise
    else:
        raise

command_index = {"update":update_system, "date":get_date, "open_program":open_program}

def execute_toolbox_commands(commands_list, special_clauses, ner_function):
    toolbox_logger.debug(f"Executing commands: {commands_list}")
    special_clauses_index = -1
    for command in commands_list:
        try:
            action = command_index.get(command)
            if command == "open_program":
                special_clauses_index += 1
                action(ner_function, special_clauses, special_clauses_index)
            else:
                action()
        except ToolboxError:
            pass