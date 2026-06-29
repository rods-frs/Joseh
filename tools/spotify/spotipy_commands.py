from dotenv import load_dotenv, set_key
import os
import logging
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from core.error_handler import SpotifyError, SpotifyTrackNotFound
from spotipy import SpotifyException

#configure logger
spotify_logger = logging.getLogger("SP")

#credential stuff

def check_credential():
    try:
        spotify_logger.debug("Checking .env for user spotify credential")
        load_dotenv()
        credential_present = True if os.getenv("SPOTIFY_CLIENT_ID") else False
        if credential_present:
            spotify_logger.debug("Credential found!")
            return True
        else:
            spotify_logger.debug("Credential is not present")
            return False
    except Exception as e:
        raise SpotifyError(f"Error while checking the user credentials: {e}")

def create_credential():
    try:
        spotify_logger.info("Starting Spotify credential creation")
        client_id = str(input("Please type your cliend ID: "))
        client_secret = str(input("Now, please type the secret: "))
        credentials_correct = False
        while credentials_correct == False:
            user_response = str(input(f"Please check the credentials. Are they correct?\nclient_id: {client_id}\nclient_secret: {client_secret}\n(y/n)>> "))
            if user_response.lower() == "y":
                spotify_logger.info("User confirmed the credentials")
                try:
                    set_key(".env", "SPOTIFY_CLIENT_ID", client_id)
                    set_key(".env", "SPOTIFY_CLIENT_SECRET", client_secret)
                    spotify_logger.debug("Local variables set successfully")
                    credentials_correct = True
                except Exception as e:
                    spotify_logger.error(f"Failed to load the credentials into the .env: {e}")
            elif user_response.lower() == "n":
                spotify_logger.debug("User did not confirmed the credentials.")
    except Exception as e:
        raise SpotifyError(f"Failed to create the user credentials: {e}")
    return True if credentials_correct else False

def spotipy_configuration(USER_REDIRECT_URL="http://127.0.0.1:8888/callback"):
    try:
        spotify_logger.debug("Configuring Spotipy API")
        global sp
        USER_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
        USER_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=USER_CLIENT_ID,
        client_secret=USER_CLIENT_SECRET,
        redirect_uri=USER_REDIRECT_URL,
        scope="user-modify-playback-state user-read-playback-state user-library-read playlist-read-private"
        ))
    except Exception as e:
        raise SpotifyError(f"Failed to configure Spotipy: {e}")

#command list
def spotify_command_list():
    spotify_logger.debug("Creating command list")
    global track_name, command_map
    track_name = ""
    command_map = {
        "resume":resume_track,
        "pause":pause_track,
        "next":next_track,
        "previous":previous_track,
        "get_music":get_current_track,
        "play_music":play_music
    }

#spotify commands
def get_current_track():
    try:
        spotify_logger.debug("Getting playing track")
        current = sp.current_playback()
        if current is not None:
            current_track = current["item"]["name"]
            spotify_logger.debug(f"track name: {current_track}")
            return current_track
        else:
            raise SpotifyError(f"Can`t get the playing track because there`s no session.")
    except Exception as e:
        raise SpotifyError(f"Failed to get the playing track name: {e}")

def resume_track():
    try:
        spotify_logger.debug("Resuming track")
        current = sp.current_playback()
        if current is not None and not current["is_playing"]:
            sp.start_playback()
            return True
        else:
            raise SpotifyError("Error while resuming track: There`s no session or the track is already playing")
    except Exception as e:
        raise SpotifyError(f"Error while resuming track: {e}")

def next_track():
    try:
        spotify_logger.debug("Skipping track")
        current = sp.current_playback()
        if current is not None:
            sp.next_track()
            return True
        else:
            raise SpotifyError("Error while skipping track: There`s no session")
    except Exception as e:
        raise SpotifyError(f"Error while skipping track: {e}")

def pause_track():
    try:
        spotify_logger.debug("Pausing track")
        current = sp.current_playback()
        if current is not None and current["is_playing"]:
            sp.pause_playback()
            return True
        else:
            raise SpotifyError("Failed to pause playback: There`s no session or the track is already paused")
    except Exception as e:
        raise SpotifyError(f"Failed to pause playback: {e}")

def previous_track():
    try:
        spotify_logger.debug("Going back one track")
        current = sp.current_playback()
        if current is not None:
            sp.previous_track()
            return True
        else:
            raise SpotifyError("Failed to go to previous track: No session")
    except Exception as e:
        raise SpotifyError(f"Failed to go to previous track: {e}")

def play_music(play_music_idx, special_clauses, ner_function):
    text = special_clauses[play_music_idx]
    music_name = ner_function(text, "music")
    track_id = get_track_id(music_name)
    play_track(track_id)
    return music_name

def play_track(uri):
    spotify_logger.debug(f"Trying to play the track with the URI: {uri}")
    try:
        sp.start_playback(uris=[uri])
        track = sp.track(uri)
        name = track["name"]
        return name
    except Exception as e:
        raise SpotifyError(f"Failed to play the track: {e}")

def get_track_id(name):
    spotify_logger.debug(f"Getting the ID of the track: {name}")
    try:
        results = sp.search(q=name, type="track", limit=1)
        track_uri = results["tracks"]["items"][0]["uri"]
        spotify_logger.debug("URI found!")
        return track_uri
    except SpotifyException as e:
        if e.http_status == 404:
            raise SpotifyTrackNotFound(f"The track with the name '{name}' was not found")
    except Exception as e:
        raise SpotifyError(f"Failed to get the track URI: {e}")

def execute_spotify_commands(commands_list, special_clauses, ner_function):
    spotify_logger.debug(f"Executing commands: {commands_list}")

    play_music_idx = 0 #this is used to make the play_music take the correct clause with the correct music request

    for command in commands_list:
        action = command_map.get(command)
        try:
            if command == 'play_music':
                result = action(play_music_idx, special_clauses, ner_function)
                play_music_idx += 1
                print(f"Now playing: {result}")
            else:
                result = action()
                if result:
                    if command == 'get_music':
                        print(f"Now playing: {result}")
        except SpotifyError:
            pass

