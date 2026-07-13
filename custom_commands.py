#configutation zone - DO NOT MODIFY
import logging
from core.error_handler import CustomCommandError
cc_logger = logging.getLogger("CC")

#commands zone - Put your custom functions here

def exampleCommand():
    try:
        print("Example command! Hello world!")
    except Exception as e:
        CustomCommandError("Nasty error here")

#commands index - Modify this part putting the index number + the command function following the example:

commands_map = {1 : exampleCommand} #please dont modify the name or delete the variable, only modify the contents adding your index number + function

#command executer - DO NOT MODIFY

def custom_command_executer():
    cc_logger.info("Entering custom command mode. Type 'exit' to leave")
    valid_command = False
    while not valid_command:
        user_command = int(input("Type the number code of your command: "))
        for key, value in commands_map.items():
            if user_command == key: 
                value()
                valid_command = True
        if not valid_command: CustomCommandError("The code {user_command} is not a valid code. Please try again or type 'exit'.")