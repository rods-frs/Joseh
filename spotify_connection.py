#Testing and developing the spotify integration

#packages
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import spacy
import re
from time import sleep

#auth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="f4dbb04636f34cd183867be4aa645af4",
    client_secret="fa271815bd414006a69636ea96813bfe",
    redirect_uri="http://127.0.0.1:8888/callback",
    scope = "user-modify-playback-state user-read-playback-state user-library-read playlist-read-private"
))

#basic commands

def resume_music(sp):
    current = sp.current_playback()
    if current is not None and not current["is_playing"]:
        sp.start_playback()
    else: print("There`s already a playback running")

def next_track(sp):
    current = sp.current_playback()
    if current is not None:
        sp.next_track()
    else: print("There`s no playback running")

def pause_music(sp):
    current = sp.current_playback()   
    if current["is_playing"]:
        sp.pause_playback()
    else: print("There`s no active playback to be paused")

def get_current_music(sp):
    current = sp.current_playback()
    if current["is_playing"]:
        track = current["item"]
        print(f"Current music: {track["name"]}")
    else: print("There`s no music playing")

def shuffle(sp, shuffle_bool):
    if shuffle_bool: #0 to turn off, 1 to turn on
        sp.shuffle(state=True)
    else: sp.shuffle(state=False)
    
def repeat(sp, repeat_bool):
    if repeat_bool:
        sp.repeat(state="track")
    else:
        sp.repeat(state="off")

def play_music(sp, uri):
    sp.start_playback(uris=[uri])

def play_playlist(sp, uri):
    sp.start_playback(context_uri=uri)

#complex commands

def music_search(sp, music_name):
    results = sp.search(q=music_name, type="track", limit=5)
    tracks = results["tracks"]["items"]
    idx1 = 0
    search_results = {}
    for track in tracks:
        idx1 += 1
        search_results[f"track_{idx1}"] = {
            "track":track["name"],
            "uri":track["uri"]
        }
    return search_results

def playlist_search(sp, playlist_name):
    results = sp.search(q=playlist_name, type="playlist", limit=5)
    playlists = [p for p in results["playlists"]["items"] if p is not None] #Ensures that the playlist is not regional locked
    idx1 = 0
    search_results = {}
    for playlist in playlists:
        idx1 += 1
        search_results[f"playlist_{idx1}"] = {
            "playlist":playlist["name"],
            "uri":playlist["uri"]
            }
    return search_results

def direct_play_playlist(sp, playlist_name):
    playlist_search_results = playlist_search(sp, playlist_name)
    for key, value in playlist_search_results.items():
        if key == "playlist_1":
            to_play_playlist_uri = value["uri"]
            to_play_playlist_name = value["playlist"]
            print(to_play_playlist_name)

    #confirming if the user wants to play the playlist coming from the search
    playlist_confirmation = int(input(f"PLayling playlist: {to_play_playlist_name}. Type 1 if OK, anything else if NO: "))
    if playlist_confirmation == 1:
        play_playlist(sp, to_play_playlist_uri)

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

#NLP usage

intention_map = {
    "resume_music":    resume_music,
    "next_track":      next_track,
    "pause_music":     pause_music,
    "shuffle":         shuffle, #requires training to check if the user wants to turn on or off
    "repeat":          repeat, #requires training to check if the user wants to turn on or off
    "get_current_music": get_current_music,
}

nlp = spacy.load("spotify-model-v1")

while True:

    usr_intention = str(input("Whats your command? >> "))

    clauses = split_usr_command(usr_intention)
    detected = []

    for clause in clauses:
        doc = nlp(clause)

        for intent, score in doc.cats.items():
            if score >= 0.5:
                print(f"Intent {intent} added!")
                detected.append(intent)

    print("="*10)

    for intention in detected:
        action = intention_map.get(intention)

        if action:
            action(sp)
            print(f"Executing command: {intention}")
            sleep(0.5)

        

