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

def setup():
    try:
        logger_configuration()
        logger.info("Starting Joseh setup.")
        load_models()
        os_recognition()
        global r
        r = speech_recognition_configuration()
        tts_configuration()

        check_and_create_spotify_credentials()
        check_and_create_system_credentials()

        logger.debug("All set!")

        return r
    except Exception as e:
        logger.critical(f"Failed to start basic Joseh features: {e}")

def load_spotify_credentials():
    client_id = str(input("Please type the client ID from your app created at developer.spotify.com: "))
    client_secret = str(input("Now, type the client secret: "))
    try: 
        set_key(".env", "SPOTIFY_CLIENT_ID", client_id)
        set_key(".env", "SPOTIFY_CLIENT_SECRET", client_secret)
        logger.debug("Local variables set successfully")
    except Exception as e:
        logger.error(f"Failed to set env variables: {e}")

def mute_joseh():
    global joseh_muted
    joseh_muted = True

def logger_configuration():
    global logger
    logger = logging.getLogger("toolbox")

def check_and_create_system_credentials():

    try:
        logger.debug("Checking for user password in system keyring...")
        global USER_PASSWORD
        USER_PASSWORD = keyring.get_password("joseh", "system_password")
        if not USER_PASSWORD:
            logger.warning("User password is not in the keyring.")
            talk_and_print("I saw that you didn`t set your system password, without it I can`t execute sudo operations like to update your system. The password will be kept in your OS keyring.")
            talk("Could you please write your password?")
            while True:
                user_response = str(input("Could you please write your password? (y/n) >> "))
                if user_response.lower() == "y": 
                    talk_and_print("Ok! now type your password, and don`t worry, your password will be kept in your OS keyring.")
                    USER_PASSWORD = str(input("Please type your password: "))
                    keyring.set_password("joseh", "system_password", USER_PASSWORD)
                    logger.debug("Password was sent to the keyring")
                    break
                elif user_response == "n":
                    logger.warning("User opted to not give the system password.")
                    break
                else: logger.error(f"The input {user_response} is not valid, please try again.")
        else: logger.debug("User password found!")
    except Exception as e:
        logger.error(f"Failed to process user password from the keyring: {e}")

def check_and_create_spotify_credentials():
    try:
        load_dotenv()
        logger.debug("Checking .env for the Spotify credentials")
        sp_client_id = os.getenv("SPOTIFY_CLIENT_ID")
        if sp_client_id:
            spotipy_configuration()
            logger.debug("Credentials found!")
        else:
            while True:
                logger.warning("Couldnt find the Spotify credentials within the .env.")
                user_input2 = input("Couldnt find your Spotify credentials. Would you like to enter your credentials? (y/n) >> ")
                if user_input2.lower() == "y":
                    logger.debug("User opted to enter the credentials")
                    load_spotify_credentials()
                    break
                elif user_input2.lower() == "n": 
                    logger.warning("User opted to not pass Spotify credentials. Spotify functions will not work")
                    break
                else:
                    logger.warning(f"{user_input2} is not a valid option. Please try again.")
    except Exception as e: logger.error(f"Error in the check_and_create_spotify_credentials: {e}")

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
    logger.debug("Loading NLP models")
    try:
        global BASE_NLP
        global CAT_MODEL
        global NER_MODEL
        BASE_NLP = spacy.load('en_core_web_lg')
        CAT_MODEL = spacy.load(r'joseh_cat_model_v2')
        NER_MODEL = spacy.load(r'joseh_ner_model_v2')
    except Exception as e:
        logger.error(f"Failed to load the models: {e}")

def os_recognition():
    global OS
    logger.debug("Recognizing OS")
    plataform = platform.system()
    if plataform == "Linux":
        OS = distro.name()
    else:
        OS = "windows"
    logger.debug(f"Recognized OS: {OS}")
    
def speech_recognition_configuration():
    logger.debug("Configuring speech recognition")
    r = sr.Recognizer()
    r.pause_threshold = 3
    return r

def tts_configuration():
    logger.debug("Configuring t2s")
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
    logger.debug("Update system function called")
    talk_and_print( "Checking and updating system")

    if "Fedora" in OS:
        command = ["sudo", "-S", "dnf", "upgrade", "-y"]
    elif "Ubuntu" in OS:
        command = ["sudo", "-S", "sh", "-c", "apt-get update && apt-get upgrade -y"]
    elif "Arch" in OS:
        command = ["sudo", "-S", "pacman", "-Syu", "--noconfirm"]
    else:
        logger.error("OS not supported for this command.")
    try:
        subprocess.run(command,input=f"{USER_PASSWORD}\n",text=True,capture_output=True,check=True)
        logger.info("System updated!")
        talk_and_print("Done! Your system is fully updated")
    except subprocess.CalledProcessError as e:
        print(f"Command failed with exit code {e.returncode}")
        print(f"--- STDOUT --- \n{e.stdout}")
        print(f"--- STDERR --- \n{e.stderr}")
        raise e

def get_date():
    logger.debug("Getting today`s date")
    today_str = date.today().strftime("%A, %d de %B de %Y")
    talk_and_print(f"Today is {today_str}")

def open_program(name):
    logger.info(f"Trying to open the program: {name}")
    talk_and_print(f"Trying to open the program: {name}")
    try:
        subprocess.Popen([name],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,preexec_fn=os.setsid)
        talk_and_print(f"{name} is now open")
    except Exception as e:
        logger.error(f"Failed to open application: {e}")
        talk_and_print(f"Failed to execute the program {name}: {e}")

#spotify commands

def get_music():
    current = sp.current_playback()
    if current is not None:
        current_track = current["item"]["name"]
        talk_and_print(f"The current music is: {current_track}")
    else:
        talk_and_print("There's nothing playing right now")
        logger.error("Error to check current music: No playback")

def resume_music():
    current = sp.current_playback()
    if current is not None and not current["is_playing"]:
        talk_and_print( "Resuming music")
        logger.info("Resuming music")
        sp.start_playback()
    else:
        talk_and_print( "Failed to resume music: No playback or track already playing")
        logger.error("Error while resuming music")

def next_track():
    current = sp.current_playback()
    if current is not None:
        talk_and_print( "Skipping this song")
        logger.info("Skipping song")
        sp.next_track()
    else:
        talk_and_print( "There's no music playing to skip")
        logger.error("Failed to skip song: No playback")

def pause_music():
    current = sp.current_playback()
    if current is not None and current["is_playing"]:
        talk( "Pausing music...")
        logger.info("Pausing music")
        sp.pause_playback()
    else:
        talk( "There's no music playing to pause")
        logger.error("Failed to execute pause command: No playback")

def previous_track():
    current = sp.current_playback()
    if current is not None:
        talk( "Playing the previous song")
        logger.info("Going back to the previous track")
        sp.previous_track()
    else:
        talk_and_print("There's no playback")
        logger.error("Failed to execute previous music command: No playback")

def play_music(uri):
    sp.start_playback(uris=[uri])
    track = sp.track(uri)
    name = track["name"]
    logger.info(f"Playing music: {name}")
    talk_and_print(f"Now playing: {name}")

#modules

def split_usr_command(text):
    logger.debug("Splitting user command...")
    parts = re.split(r'\b(and then|and|also|then)\b|(\s*,\s*)', text, flags=re.IGNORECASE)
    clean_parts = []
    for p in parts:
        if p is None:
            continue
        p = p.strip()
        if p and p.lower() not in ('and', 'then', 'and then', 'also',',', ''):
            logger.debug(f"Adding part to clean_parts: {p}")
            clean_parts.append(p)
    return clean_parts

def execute_spotify_commands(commands_list, commands_map):
    for command in commands_list:
        action = commands_map.get(command)
        action()

def intent_recognition(usr_input):
        logger.debug("Trying to detect user intention.")
        try:
            clauses = split_usr_command(usr_input)
            detected = []
            for clause in clauses:
                doc = CAT_MODEL(clause)
                for intent, score in doc.cats.items():
                    if score >= 0.5:
                        logger.debug(f"Intent {intent} added!")
                        logger.debug(f"Intent recognized: {intent}")
                        detected.append(intent)
            if len(detected) >= 1: return detected
            else:
                logger.error("No intention were detected.")
                return None
        except Exception as e:
            logger.error(f"Couldn`t detect the user intention: {e}")

def check_simple_command(commands_map, text):
    logger.debug("Checking if user command is simple... ")
    doc = BASE_NLP(text)
    complex_command_detected = False
    detected_commands = []
    for ent in doc.ents:
        if ent.text:
            complex_command_detected = True
            logger.debug(f"Entity detected: {ent.text}")
    if not complex_command_detected:
        for token in doc:
            logger.debug(f"Lemma analyzed: {token.lemma_}")
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
            logger.warning("The program name was recognized as a music")
        detected = ent.text
        logger.debug(f"The name recognized was: {detected}")
        break
    if not detected:
        logger.error("The name was not recognized. the variable DETECTED will return None")
        return None
    else:
        return detected

def get_music_name(text):
    detected = ""
    doc = NER_MODEL(text)
    for ent in doc.ents:
        if ent.label_ == "program":
            logger.warning("The music name was recognized as a program")
        detected = ent.text
        logger.debug(f"The name recognized was: {detected}")
        break
    if not detected:
        logger.error("The name was not recognized. the variable DETECTED will return None")
        return None
    else:
        return detected

def get_music_id(name):
    logger.debug(f"Getting the ID of the music: {name}")
    try:
        results = sp.search(q=name, type="track", limit=1)
        track_uri = results["tracks"]["items"][0]["uri"]
        logger.debug("URI found!")
        return track_uri
    except Exception as e:
        logger.error(f"Failed to get the music URI: {e}")
        return None

def hear_user(SPEECH_WAIT_TIME):
    logger.debug("Trying to hear the user")
    try:
        logger.info("Now hearing the user.")
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source, phrase_time_limit=SPEECH_WAIT_TIME)
        usr_input = r.recognize_google(audio, language="en_US")
        logger.debug(f"Recognized phrase: {usr_input}")
        return usr_input
    except Exception as e:
        logger.error(f"Failed to hear the user: {e}")

def wait_for_wake_word(wake_word, SPEECH_WAIT_TIME=5):
    logger.debug(f"Waiting for wake word: {wake_word}")
    wake_word_detected = False
    while not wake_word_detected or user_input.lower() != "cancel":
        logger.debug("Stating new hearing round.")
        user_input = hear_user(SPEECH_WAIT_TIME)
        if user_input and wake_word in user_input:
            logger.info("Wake word detected!")
            wake_word_detected = True
            break
        elif user_input and user_input.lower() == "cancel":
            logger.info("User canceled hearing round")
            wake_word_detected = "CANCEL"
            break
            break
        else:
            logger.debug("The wake word was not detected in this hearing round.")
    return wake_word_detected