#packages
import spacy
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import logging
from time import sleep
import re
import subprocess
import speech_recognition as sr
import pyttsx3
from datetime import date
import platform
import distro

#alsa error handler (made by AI)
import os
import ctypes

ERROR_HANDLER_FUNC = ctypes.CFUNCTYPE(None, ctypes.c_char_p, ctypes.c_int,
                                       ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p)
def py_error_handler(filename, line, function, err, fmt):
    pass

c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)
asound = ctypes.cdll.LoadLibrary('libasound.so.2')
asound.snd_lib_error_set_handler(c_error_handler)

#configuration

def setup():
    logging = logging_configuration()
    sp = spotipy_configuration()
    base_model, joseh_model = load_models()
    OS = os_recognition()
    r = speech_recognition_configuration()
    engine = tts_configuration()

    return logging, sp, base_model, joseh_model, OS, r, engine

def logging_configuration():
    logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    return logging

def spotipy_configuration():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="f4dbb04636f34cd183867be4aa645af4",
    client_secret="fa271815bd414006a69636ea96813bfe",
    redirect_uri="http://127.0.0.1:8888/callback",
    scope="user-modify-playback-state user-read-playback-state user-library-read playlist-read-private"
    ))
    return sp

def load_models():
    logging.debug("Loading NLP models")
    base_nlp = spacy.load('en_core_web_lg')
    joseh_model = spacy.load(r'joseh_model_v1')
    return base_nlp, joseh_model

def os_recognition():
    logging.debug("Recognizing OS")
    plataform = platform.system()
    if plataform == "Linux":
        OS = distro.name()
    else:
        OS = "windows"
    logging.debug(f"Recognized OS: {OS}")
    return OS

def speech_recognition_configuration():
    logging.debug("Configuring speech recognition")
    r = sr.Recognizer()
    r.pause_threshold = 3
    return r

def tts_configuration():
    logging.debug("Configuring t2s")
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # default is 200
    return engine

def talk_and_print(engine, text):
    engine.say(text)
    engine.runAndWait()
    print(text)

def talk(engine, text):
    engine.say(text)
    engine.runAndWait()

#system commands

def update_system(OS, password, engine):
    logging.debug("Update system function called")
    talk_and_print(engine, "Checking and updating system")
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

def get_date(engine):
    today_str = date.today().strftime("%A, %d de %B de %Y")
    talk_and_print(engine, f"Today is {today_str}")

#spotify commands

def get_music(engine, sp):
    current = sp.current_playback()
    if current is not None:
        current_track = current["item"]["name"]
        talk_and_print(engine, f"The current music is: {current_track}")
    else:
        talk_and_print(engine, "There's nothing playing right now")
        logging.error("Error to check current music: No playback")

def resume_music(engine, sp):
    current = sp.current_playback()
    if current is not None and not current["is_playing"]:
        talk_and_print(engine, "Resuming music")
        logging.info("Resuming music")
        sp.start_playback()
    else:
        talk_and_print(engine, "Failed to resume music: No playback or track already playing")
        logging.error("Error while resuming music")

def next_track(engine, sp):
    current = sp.current_playback()
    if current is not None:
        talk_and_print(engine, "Skipping this song")
        logging.info("Skipping song")
        sp.next_track()
    else:
        talk_and_print(engine, "There's no music playing to skip")
        logging.error("Failed to skip song: No playback")

def pause_music(engine, sp):
    current = sp.current_playback()
    if current is not None and current["is_playing"]:
        talk(engine, "Pausing music...")
        logging.info("Pausing music")
        sp.pause_playback()
    else:
        talk(engine, "There's no music playing to pause")
        logging.error("Failed to execute pause command: No playback")

def previous_track(engine, sp):
    current = sp.current_playback()
    if current is not None:
        talk(engine, "Playing the previous song")
        logging.info("Going back to the previous track")
        sp.previous_track()
    else:
        talk_and_print(engine, "There's no playback")
        logging.error("Failed to execute previous music command: No playback")

#complex modules

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

def execute_spotify_commands(commands_list, commands_map):
    for command in commands_list:
        action = commands_map.get(command)
        action()

def intent_recognition(usr_input, joseh_model, engine):
        logging.debug("Complex command detected! Passing input to Joseh Model...")
        clauses = split_usr_command(usr_input)
        detected = []
        for clause in clauses:
            doc = joseh_model(clause)
            for intent, score in doc.cats.items():
                if score >= 0.5:
                    logging.debug(f"Intent {intent} added!")
                    logging.debug(f"Intent recognized: {intent}")
                    detected.append(intent)
        return detected

def check_simple_command(commands_map, base_model, text):
    logging.debug("Checking if user command is simple... ")
    doc = base_model(text)
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


