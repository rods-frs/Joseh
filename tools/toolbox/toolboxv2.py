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
        updated_packages = []
        for line in result.stdout.splitlines():
            if "upgrading" in line.lower():
                updated_packages.append(line.removeprefix("upgrading "))
        if len(updated_packages) <= 1:
            toolbox_logger.info("System is already updated")
        else:
            print("Packages updated:")
            for package in updated_packages:
                print(package)
        toolbox_logger.info("Update finished.")
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
        installed_flatpaks_raw = subprocess.run(name_command,text=True,capture_output=True,check=True)
        installed_flatpaks = []
        times_ran = 0
        for line in installed_flatpaks_raw.stdout.splitlines():
            if times_ran != 0:
                installed_flatpaks.append(line)
            times_ran += 1
    except Exception as e:
        raise FlatpakModuleError(f"stderr: {getattr(e, 'stderr', 'N/A')}")

def start_flatpak_program(program):
    try:
        #try to find the program in the installed program list
        program_found = False
        toolbox_logger.debug(f"Trying to find a Flatpak by the name {program}")
        for package in installed_flatpaks:
            if program in package.lower():
                toolbox_logger.debug(f"Package found: {package}")
                program_found = True
                execution_command = ["flatpak", "run", package]
                try:
                    toolbox_logger.debug(f"Trying to execute the program by the ID {package}")
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

def search_flatpak(package_name):
    search_command = ['flatpak', 'search', '--columns=application', package_name]
    try:
        toolbox_logger.debug(f"Searching for Flatpak {package_name}")
        query_result = subprocess.run(search_command, capture_output=True, text=True, check=True)
        query_result = query_result.stdout.splitlines()
        package_id = ""
        for package in query_result:
            if package_name.lower() in package.lower():
                package_id = package
        if package_id: 
            toolbox_logger.debug("Package found!")
            return package_id
        else: return None
    except Exception as e:
        raise FlatpakModuleError(f"Failed to search for the package {package_name}: {getattr(e, 'stderr', 'N/A')} | error: {e}")
        
def install_flatpak(package_id):
    install_command = ['flatpak', 'install', '-y', package_id]
    try:
        toolbox_logger.info(f"Trying to install app by the ID {package_id}...")
        subprocess.run(install_command, text=True, capture_output=True, check=True)
        toolbox_logger.info(f"Package installed!")
    except Exception as e:
        FlatpakModuleError(f"Failed to install the package: stderr: {getattr(e, 'stderr', 'N/A')} | error: {e}")

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