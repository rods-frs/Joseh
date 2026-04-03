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

def shuffle_on(sp):
    sp.shuffle(state=True)

def shuffle_off(sp):
    sp.shuffle(state=False)
    
def repeat_on(sp):
    sp.repeat(state="track")

def repeat_off(sp):
    sp.repeat(state="off")

def play_music(sp, uri):
    sp.start_playback(uris=[uri])

def play_playlist(sp, uri):
    sp.start_playback(context_uri=uri)

#base commands

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

#composite commands

def direct_playlist_play(sp, usr_input):

    playlist_name = get_playlist_name(usr_input)
    if playlist_name is not None:
        playlist_search_results = playlist_search(sp, playlist_name)

        for key, value in playlist_search_results.items():
            if key == "playlist_1":
                to_play_playlist_uri = value["uri"]
                to_play_playlist_name = value["playlist"]

        print(f"Playing {to_play_playlist_name}")
        play_playlist(sp, to_play_playlist_uri)
    else: print("Playlist name not found...")

def direct_music_play(sp, usr_input):

    music_name = get_music_name(usr_input)
    search_results = music_search(sp, music_name)

    for key, value in search_results.items():
        if key == "track_1":
            m_play = value["uri"]
            m_name = value["track"]

    print(f"Playing {m_name}")
    play_music(sp, m_play)

def get_music_name(usr_input):
    ner_nlp = spacy.load("NER_MODEL")
    doc = ner_nlp(usr_input)
    for ent in doc.ents:
        if ent.label_ == "MUSIC_NAME":
            print(ent.text)
            music_name = ent.text
            return music_name

def get_playlist_name(usr_input):
    ner_nlp = spacy.load("NER_MODEL_2")
    doc = ner_nlp(usr_input)
    for ent in doc.ents:
        if ent.label_ == "playlist_name":
            print(ent.text)
            playlist_name = ent.text
            return playlist_name

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
    "shuffle_off":     shuffle_off, 
    "repeat_on":        repeat_on, 
    "repeat_off":       repeat_off,
    "get_current_music": get_current_music,
    "shuffle_on":       shuffle_on,
    "play_music":       direct_music_play,
    "play_playlist":    direct_playlist_play,
    "search_music":     music_search,   #not done
    "search_playlist":  playlist_search  #not done
}


nlp = spacy.load("spotify-v2")


while True:

    usr_intention = str(input("Whats your command? >> "))

    try:
        clauses = split_usr_command(usr_intention)
        detected = []
        found_intent = False

        for clause in clauses:
            doc = nlp(clause)
            clause = str(clause)

            for intent, score in doc.cats.items():
                if score >= 0.5:

                    if intent == "shuffle":
                        if "on" in clause: 
                            detected.append("shuffle_on")
                        else:
                            detected.append("shuffle_off")

                    elif intent == "repeat":
                        if "on" in clause: 
                            detected.append("repeat_on")
                        else:
                            detected.append("repeat_off")

                    elif intent != "none":
                        print(f"Intent {intent} added!")
                        detected.append(intent)

                    found_intent = True

            if not found_intent:
                print("No intent for your command was found... ")
                        

        print("="*10)

        for intention in detected:
            action = intention_map.get(intention)

            if action:
                if intention == "play_music" or intention == "play_playlist":
                    action(sp, usr_intention)
                else:
                    print(intention)
                    action(sp)
                print(f"Executing command: {intention}")
                print("=-="*8)
                sleep(0.5)
    except Exception as e:
        print(f"Error: {e}")





