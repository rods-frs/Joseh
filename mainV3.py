#packages
import spacy
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from os import system as sy
<<<<<<< Updated upstream
import logging
=======
import os
import logging
from time import sleep
import re
import subprocess
>>>>>>> Stashed changes

#logging configuration
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

#spotify auth
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="f4dbb04636f34cd183867be4aa645af4",
    client_secret="fa271815bd414006a69636ea96813bfe",
    redirect_uri="http://127.0.0.1:8888/callback",
    scope="user-modify-playback-state user-read-playback-state user-library-read playlist-read-private"
))

#nlp models loading
BASE_NLP = spacy.load('en_core_web_lg')
<<<<<<< Updated upstream

#global variables
OS = "fedora"

#system commands
def update_system():
    if OS == "fedora":
        logging.info("Updating system... ")
        sy("sudo -S dnf -y update > /dev/null")
    else: 
        logging.info("The only OS supported for this command is RedHat based systems.")

def get_date():
    date = sy("date")
    print(f"Today`s date is: {date}")
=======
joseh_model = spacy.load('/home/rodrigo/PycharmProjects/Joseh/model_training/joseh_model_v1')

#global variables
password = os.environ.get("JOSEH_SUDO_PASS")
print(password)
OS = "ubuntu"

#system commands
def update_system():
    print(repr(password))
    if OS == "fedora":
        logging.info("Updating system...")
        subprocess.run(["sudo", "-S", "dnf", "-y", "update"], input=f"{password}\n", text=True)
        logging.info("System updated!")
    elif OS == "ubuntu":
        logging.info("Updating system...")
        subprocess.run(["sudo", "-S", "apt", "update"], input=f"{password}\n", text=True)
        subprocess.run(["sudo", "-S", "apt", "-y", "upgrade"], input=f"{password}\n", text=True)
        logging.info("System updated!")
    else:
        logging.info("OS not supported for this command.")


def get_date():
    sy("date")
>>>>>>> Stashed changes

#spotify commands
def resume_music():
    current = sp.current_playback()
    if current is not None and not current["is_playing"]:
        sp.start_playback()
    else:
        print("There`s already a playback running")

def next_track():
    current = sp.current_playback()
    if current is not None:
        sp.next_track()
    else:
        print("There`s no playback running")

def pause_music():
    current = sp.current_playback()
    if current["is_playing"]:
        sp.pause_playback()
    else:
        print("There`s no active playback to be paused")

def previous_track():
    sp.previous_track()

#command mapping
commands_map = {
    "resume": resume_music,
    "pause": pause_music,
    "skip": next_track,
    "next": next_track,
    "back": previous_track,
    "previous": previous_track,
    "update": update_system,
    "date": get_date
}

#modules
def check_simple_command(text):
    logging.debug("Checking if user command is simple... ")
    doc = BASE_NLP(text)
    complex_command_detected = False
    detected_commands = []
    for ent in doc.ents:
        if ent.text:
            complex_command_detected = True
            logging.debug(f"Entity detected: {ent.text}")
    if not complex_command_detected:
        for token in doc:
            logging.debug(f"Lemma analyzed: {token.lemma_}")
            if token.lemma_ in commands_map:
                detected_commands.append(token.lemma_)
    if not complex_command_detected and len(detected_commands) >= 1:
        return True, detected_commands
    else:
        return False, "null"

<<<<<<< Updated upstream
=======
def split_usr_command(text):
    parts = re.split(r'\b(and then|and|also|then)\b|(\s*,\s*)', text, flags=re.IGNORECASE)
    clean_parts = []
    for p in parts:
        if p is None:
            continue
        p = p.strip()
        if p and p.lower() not in ('and', 'then', 'and then', 'also',',', ''):
            clean_parts.append(p)
    return clean_parts

>>>>>>> Stashed changes
def execute_spotify_commands(commands_list):
    for command in commands_list:
        action = commands_map.get(command)
        action()

#main loop
while True:
<<<<<<< Updated upstream
=======
    sleep(1)
>>>>>>> Stashed changes
    usr_input = str(input(">>> "))
    if usr_input == "exit":
        logging.info("== USER EXIT ==")
        break
    simple_command, command_list = check_simple_command(usr_input)
    if simple_command:
        logging.debug("Simple command detected!")
        execute_spotify_commands(command_list)
    else:
<<<<<<< Updated upstream
        logging.info("complex command detected! ignoring...")
=======
        logging.debug("Complex command detected! Passing input to Joseh Model...")
        clauses = split_usr_command(usr_input)
        detected = []
        for clause in clauses:
            doc = joseh_model(clause)
            for intent, score in doc.cats.items():
                if score >= 0.5:
                    print(f"Intent {intent} added!")
                    detected.append(intent)
        if len(detected) < 0:
            logging.debug("No intents detected!")
        else:
            print("=" * 10)
            for intention in detected:
                action = commands_map.get(intention)
                if action:
                    action()
                    print(f"Executing command: {intention}")
                    sleep(0.5)
>>>>>>> Stashed changes
