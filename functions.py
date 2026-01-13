#imports
import spacy
from os import system
import subprocess

#functions

def get_verb(doc):
    for token in doc:
        if token.pos_ == "VERB" or (token.pos_ == "ADJ" and token.text.lower() in ["open", "close"]):
            return token
    return None

def get_obj(doc):
    for token in doc:
        if token.dep_ == "dobj":
            return token
    return None

def get_p_path(p_name):
    raw_location = subprocess.check_output(f"whereis {p_name}", shell=True, text=True)
    raw_location = raw_location.splitlines()
                    
    # Parse output and extract path
    _, _, after = raw_location[0].partition(":")
    if len(after) > 1:
        return after
    return None

def open_p(p_path):
        command = f"nohup {p_path} >/dev/null 2>&1 &"
        system(command)
        return "1"

def update_sys():
    print("Starting full system update. This can take a while to finish.")
    result = subprocess.run(
        ["pacman", "-Syu", "--noconfirm"],
        stdout=subprocess.DEVNULL,   # hide standard output
        stderr=subprocess.DEVNULL    # hide error output
    )

    if result.returncode == 0:
        print("Command executed successfully")
    else:
        print("Command failed")


