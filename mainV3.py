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
import platform
import distro

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
try:
    logging.debug("Loading NLP models")
    BASE_NLP = spacy.load('en_core_web_lg')
    joseh_model = spacy.load(r'joseh_model_v1')
except Exception as e:
    logging.error(f"Error while loading NLP models: {e}")

#OS recognition
try:
    logging.debug("Recognizing OS")
    plataform = platform.system()
    if plataform == "Linux":
        OS = distro.name()
    else:
        OS = "windows"
    logging.debug(f"Recognized OS: {OS}")
except Exception as e:
    logging.error(f"Error while recognizing the OS: {e}")

#speech recognition configuration
try:
    logging.debug("Configuring speech recognition")
    r = sr.Recognizer()
    r.pause_threshold = 3
except Exception as e:
    logging.error(f"Failed to configure speech recognition: {e}")

#text to speech configuration
try:
    logging.debug("Configuring t2s")
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # default is 200
    if "windows" in OS:
        engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_ZIRA_11.0')
except Exception as e:
    logging.error(f"Failed to configure t2s: {e}")

#Global variables
SPEECH_ACTIVE = True
password = "Herocraft" 

#system commands
def update_system():
    if "Fedora" in OS:
        logging.info("Updating system...")
        subprocess.run(["sudo", "-S", "dnf", "-y", "update"], input=f"{password}\n", text=True)
        logging.info("System updated!")
    elif "ubuntu" in OS:
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
    engine.runAndWait()

#t2s functions
def talk(text):
    engine.say(text)
    engine.runAndWait()

def talk_and_print(text):
    engine.say(text)
    engine.runAndWait()
    print(text)

#spotify commands
def get_music():
    current = sp.current_playback()
    if current is not None:
        current_track = current["item"]["name"]
        talk_and_print(f"The current music is: {current_track}")
    else:
        talk_and_print("There's nothing playing right now")
        logging.error("Error to check current music: No playback")

def resume_music():
    current = sp.current_playback()
    if current is not None and not current["is_playing"]:
        talk("Resuming music")
        logging.info("Resuming music")
        sp.start_playback()
    else:
        print("Failed to resume music: No playback or track already playing")

def next_track():
    current = sp.current_playback()
    if current is not None:
        talk("Skipping this song")
        logging.info("Skipping song")
        sp.next_track()
    else:
        talk("There's no music playing to skip")
        logging.error("Failed to skip song: No playback")

def pause_music():
    current = sp.current_playback()
    if current is not None and current["is_playing"]:
        talk("Pausing music...")
        logging.info("Pausing music")
        sp.pause_playback()
    else:
        talk("There's no music playing to pause")
        logging.error("Failed to execute pause command: No playback")

def previous_track():
    current = sp.current_playback()
    if current is not None:
        talk("Playing the previous song")
        logging.info("Going back to the previous track")
        sp.previous_track()
    else:
        talk("There's no playback")
        logging.error("Failed to execute previous music command: No playback")

#command mapping
commands_map = {
    "resume": resume_music,
    "pause": pause_music,
    "next": next_track,
    "previous": previous_track,
    "update": update_system,
    "date": get_date,
    "get_music": get_music
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
    logging.debug("Splitting user command...")
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
talk_and_print("Hello, my name is Joseh, welcome!")
while True:
    correct_speech = False
    sleep(1)
    if not SPEECH_ACTIVE:
        print("="*10)
        talk_and_print("Whats your command?")
        usr_input = str(input(">>> "))
    else:
        while not correct_speech:
            #speech recognition
            talk("Press ENTER to talk to me")
            input("Press ENTER to start recognition")
            try:
                with sr.Microphone() as source:
                    talk_and_print("Im lissening")
                    r.adjust_for_ambient_noise(source, duration=1)
                    audio = r.listen(source, phrase_time_limit=10)
                usr_input = r.recognize_google(audio, language="en_US")
                print(usr_input)  # string pronta
                #usr_input2 = input("Command is correct? Y/N >> ")
                usr_input2 = "Y"
                if usr_input2 == "Y":
                    break
            except Exception as e:
                talk_and_print(f"Sorry, I didn`t understand what you said")
                logging.error(f"Error while understanding the speech: {e}")

    if usr_input == "exit":
        talk_and_print("Goodbye")
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
                    talk_and_print(f"Intent recognized: {intent}")
                    detected.append(intent)
        if len(detected) < 0:
            talk_and_print("I didnt recognized any intention")
            logging.error("No intents detected!")
        else:
            print("=" * 10)
            for intention in detected:
                action = commands_map.get(intention)
                if action:
                    talk_and_print(f"Executing command: {intention}")
                    sleep(2)
                    action()
                    

