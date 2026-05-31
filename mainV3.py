#packages
import spacy
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from os import system as sy
import os
import logging
from time import sleep
import re
import subprocess
import speech_recognition as sr
import pyttsx3
from datetime import date

#speech recognition configuration
r = sr.Recognizer()
r.pause_threshold = 3

#text to speech configuration
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # default is 200


#logging configuration
logging.basicConfig(
    level=logging.INFO,
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

joseh_model = spacy.load(r'/home/rodrigofernando/Documents/GitHub/Joseh/joseh_model_v1')

#global variables
password = os.environ.get("JOSEH_SUDO_PASS")
print(password)
OS = "fedora"
SPEECH_ACTIVE = True


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
    today_str = date.today().strftime("%A, %d de %B de %Y")
    engine.say(f"Today is {today_str}")
    print(today_str)
    engine.runAndWait


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

def execute_spotify_commands(commands_list):
    for command in commands_list:
        action = commands_map.get(command)
        action()

#main loop
engine.say("Hello, my name is Joseh, welcome!")
while True:
    
    engine.runAndWait()
    correct_speech = False
    sleep(1)
    if not SPEECH_ACTIVE:
        usr_input = str(input(">>> "))
    else:
        while not correct_speech:

            #speech recognition

            engine.say("Press ENTER to talk to me")
            engine.runAndWait()
            input("Press ENTER to start recognition")
            try:
                with sr.Microphone() as source:
                    engine.say("Im lissening")
                    print("Ouvindo...")
                    r.adjust_for_ambient_noise(source, duration=1)
                    audio = r.listen(source, phrase_time_limit=10)
                usr_input = r.recognize_google(audio, language="en_US")
                print(usr_input)  # string pronta
                #usr_input2 = input("Command is correct? Y/N >> ")
                usr_input2 = "Y"
                if usr_input2 == "Y":
                    break
            except Exception as e:
                engine.say(f"Sorry, I didn`t understand what you said")
                engine.runAndWait()
                logging.error(f"Error while understanding the speech: {e}")

    if usr_input == "exit":
        engine.say("Goodbye")
        engine.runAndWait()
        logging.info("== USER EXIT ==")
        break
    simple_command, command_list = check_simple_command(usr_input)
    if simple_command:
        logging.debug("Simple command detected!")
        execute_spotify_commands(command_list)
    else:
        logging.debug("Complex command detected! Passing input to Joseh Model...")
        clauses = split_usr_command(usr_input)
        detected = []
        for clause in clauses:
            doc = joseh_model(clause)
            for intent, score in doc.cats.items():
                if score >= 0.5:
                    print(f"Intent {intent} added!")
                    engine.say(f"Intent recognized: {intent}")
                    engine.runAndWait()
                    detected.append(intent)
        if len(detected) < 0:
            logging.debug("No intents detected!")
        else:
            print("=" * 10)
            engine.say("Executing commands")
            engine.runAndWait
            for intention in detected:
                engine.say(intention)
                engine.runAndWait
            for intention in detected:
                action = commands_map.get(intention)
                if action:
                    engine.say(f"Executing command: {intention}")
                    engine.runAndWait()
                    print(f"Executing command: {intention}")
                    sleep(2)
                    action()
                    

