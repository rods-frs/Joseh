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
import os
from dotenv import load_dotenv 
from dotenv import set_key
import keyring

#parameters
joseh_muted = False

#alsa mutter
import sys
import ctypes

if sys.platform.startswith("linux"):
    ERROR_HANDLER_FUNC = ctypes.CFUNCTYPE(None, ctypes.c_char_p, ctypes.c_int,
                                           ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p)
    def py_error_handler(filename, line, function, err, fmt):
        pass
    c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)
    asound = ctypes.cdll.LoadLibrary('libasound.so.2')
    asound.snd_lib_error_set_handler(c_error_handler)

#configuration

def load_spotify_credentials():
    client_id = str(input("Please type the client ID from your app created at developer.spotify.com: "))
    client_secret = str(input("Now, type the client secret: "))
    try: 
        set_key(".env", "SPOTIFY_CLIENT_ID", client_id)
        set_key(".env", "SPOTIFY_CLIENT_SECRET", client_secret)
        logging.debug("Local variables set successfully")
    except Exception as e:
        logging.error(f"Failed to set env variables: {e}")

def mute_joseh():
    global joseh_muted
    joseh_muted = True

def setup():
    logging = logging_configuration()
    load_models()
    os_recognition()
    r = speech_recognition_configuration()
    tts_configuration()

    #getting spotify credentials
    load_dotenv()
    try:
        logging.debug("Checking .env for the Spotify credentials")
        sp_client_id = os.getenv("SPOTIFY_CLIENT_ID")
        if sp_client_id:
            spotipy_configuration()
            logging.debug("Credentials found!")
        else:
            logging.warning("Couldnt find the Spotify credentials within the .env. Asking user for the credentials.")
            user_input2 = input("Couldnt find your Spotify credentials. Type anything to start the Spotify credential loading or press ENTER to ignore. >> ")
            if user_input2:
                load_spotify_credentials()
            else: 
                logging.warning("User opted to not pass Spotify credentials. Spotify functions will not work")
    except Exception as e: logging.error(f"It was not possible to load the variable: {e}")

    #getting user system password
    try:
        logging.debug("Checking for user password in system keyring...")
        global USER_PASSWORD
        USER_PASSWORD = keyring.get_password("joseh", "system_password")
        logging.debug(f"User password is: {USER_PASSWORD}")
        if not USER_PASSWORD:
            logging.info("User password is not in the keyring. Asking user for the password")
            talk_and_print("I saw that you didn`t set your system password, without it I can`t execute sudo operations like to update your system. The password will be kept in your OS keyring.")
            talk("Could you please write your password?")
            USER_PASSWORD = str(input("Could you please write your password? (Leave blank if no)>> "))
            if USER_PASSWORD: 
                talk_and_print("Thanks! Your password will be kept in your OS keyring")
                keyring.set_password("joseh", "system_password", USER_PASSWORD)
            else:
                talk_and_print("Nothing was wrote. Functions like update system will not work with it.")
        else: logging.debug("User password found!")
    except Exception as e:
        logging.error(f"Failed to process user password from the keyring: {e}")

    return logging, r

def logging_configuration():
    logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    return logging

def spotipy_configuration(USER_REDIRECT_URL="http://127.0.0.1:8888/callback"):
    global sp
    USER_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
    USER_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=USER_CLIENT_ID,
    client_secret=USER_CLIENT_SECRET,
    redirect_uri=USER_REDIRECT_URL,
    scope="user-modify-playback-state user-read-playback-state user-library-read playlist-read-private"
    ))

def load_models():
    logging.debug("Loading NLP models")
    try:
        global BASE_NLP
        global CAT_MODEL
        global NER_MODEL
        BASE_NLP = spacy.load('en_core_web_lg')
        CAT_MODEL = spacy.load(r'joseh_cat_model_v2')
        NER_MODEL = spacy.load(r'joseh_ner_model_v2')
    except Exception as e:
        logging.error(f"Failed to load the models: {e}")

def os_recognition():
    global OS
    logging.debug("Recognizing OS")
    plataform = platform.system()
    if plataform == "Linux":
        OS = distro.name()
    else:
        OS = "windows"
    logging.debug(f"Recognized OS: {OS}")
    
def speech_recognition_configuration():
    logging.debug("Configuring speech recognition")
    r = sr.Recognizer()
    r.pause_threshold = 3
    return r

def tts_configuration():
    logging.debug("Configuring t2s")
    global engine
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)

def talk_and_print(text):
    if not joseh_muted:
        engine.say(text)
        engine.runAndWait()
    print(text)

def talk(text):
    engine.say(text)
    engine.runAndWait()

#system commands

def update_system():
    logging.debug("Update system function called")
    talk_and_print( "Checking and updating system")

    if "Fedora" in OS:
        command = ["sudo", "-S", "dnf", "upgrade", "-y"]
    elif "Ubuntu" in OS:
        command = ["sudo", "-S", "sh", "-c", "apt-get update && apt-get upgrade -y"]
    elif "Arch" in OS:
        command = ["sudo", "-S", "pacman", "-Syu", "--noconfirm"]
    else:
        logging.error("OS not supported for this command.")
    try:
        subprocess.run(command,input=f"{USER_PASSWORD}\n",text=True,capture_output=True,check=True)
        logging.info("System updated!")
        talk_and_print("Done! Your system is fully updated")
    except subprocess.CalledProcessError as e:
        print(f"Command failed with exit code {e.returncode}")
        print(f"--- STDOUT --- \n{e.stdout}")
        print(f"--- STDERR --- \n{e.stderr}")
        raise e

def get_date():
    logging.debug("Getting today`s date")
    today_str = date.today().strftime("%A, %d de %B de %Y")
    talk_and_print( f"Today is {today_str}")

def open_program(name):
    logging.info(f"Trying to open the program: {name}")
    talk_and_print(f"Trying to open the program: {name}")
    try:
        subprocess.Popen([name],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,preexec_fn=os.setsid)
        talk_and_print(f"{name} is now open")
    except Exception as e:
        logging.error(f"Failed to open application: {e}")
        talk_and_print(f"Failed to execute the program {name}: {e}")

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
        talk_and_print( "Resuming music")
        logging.info("Resuming music")
        sp.start_playback()
    else:
        talk_and_print( "Failed to resume music: No playback or track already playing")
        logging.error("Error while resuming music")

def next_track():
    current = sp.current_playback()
    if current is not None:
        talk_and_print( "Skipping this song")
        logging.info("Skipping song")
        sp.next_track()
    else:
        talk_and_print( "There's no music playing to skip")
        logging.error("Failed to skip song: No playback")

def pause_music():
    current = sp.current_playback()
    if current is not None and current["is_playing"]:
        talk( "Pausing music...")
        logging.info("Pausing music")
        sp.pause_playback()
    else:
        talk( "There's no music playing to pause")
        logging.error("Failed to execute pause command: No playback")

def previous_track():
    current = sp.current_playback()
    if current is not None:
        talk( "Playing the previous song")
        logging.info("Going back to the previous track")
        sp.previous_track()
    else:
        talk_and_print("There's no playback")
        logging.error("Failed to execute previous music command: No playback")

def play_music(uri):
    sp.start_playback(uris=[uri])
    track = sp.track(uri)
    name = track["name"]
    logging.info(f"Playing music: {name}")
    talk_and_print(f"Now playing: {name}")

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
            logging.debug(f"Adding part to clean_parts: {p}")
            clean_parts.append(p)
    return clean_parts

def execute_spotify_commands(commands_list, commands_map):
    for command in commands_list:
        action = commands_map.get(command)
        action()

def intent_recognition(usr_input):
        logging.debug("Trying to detect user intention.")
        try:
            clauses = split_usr_command(usr_input)
            detected = []
            for clause in clauses:
                doc = CAT_MODEL(clause)
                for intent, score in doc.cats.items():
                    if score >= 0.5:
                        logging.debug(f"Intent {intent} added!")
                        logging.debug(f"Intent recognized: {intent}")
                        detected.append(intent)
            if len(detected) >= 1: return detected
            else:
                logging.error("No intention were detected.")
                return None
        except Exception as e:
            logging.error(f"Couldn`t detect the user intention: {e}")

def check_simple_command(commands_map, text):
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

def get_program_name(text):
    detected = ""
    doc = NER_MODEL(text)
    for ent in doc.ents:
        if ent.label_ == "music":
            logging.warning("The program name was recognized as a music")
        detected = ent.text
        logging.debug(f"The name recognized was: {detected}")
        break
    if not detected:
        logging.error("The name was not recognized. the variable DETECTED will return None")
        return None
    else:
        return detected

def get_music_name(text):
    detected = ""
    doc = NER_MODEL(text)
    for ent in doc.ents:
        if ent.label_ == "program":
            logging.warning("The music name was recognized as a program")
        detected = ent.text
        logging.debug(f"The name recognized was: {detected}")
        break
    if not detected:
        logging.error("The name was not recognized. the variable DETECTED will return None")
        return None
    else:
        return detected

def get_music_id(name):
    logging.debug(f"Getting the ID of the music: {name}")
    try:
        results = sp.search(q=name, type="track", limit=1)
        track_uri = results["tracks"]["items"][0]["uri"]
        logging.debug("URI found!")
        return track_uri
    except Exception as e:
        logging.error(f"Failed to get the music URI: {e}")
        return None
