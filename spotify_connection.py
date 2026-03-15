#Testing and developing the spotify integration

#packages
import spotipy
from spotipy.oauth2 import SpotifyOAuth

#auth
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="f4dbb04636f34cd183867be4aa645af4",
    client_secret="fa271815bd414006a69636ea96813bfe",
    redirect_uri="http://127.0.0.1:8888/callback",
    scope = "user-modify-playback-state user-read-playback-state user-library-read playlist-read-private"
))

#basic commands

def resume_playback(sp):
    current = sp.current_playback()
    if current is not None and not current["is_playing"]:
        sp.start_playback()
    else: print("There`s already a playback running")

def next_track(sp):
    current = sp.current_playback()
    if current is not None:
        sp.next_track()
    else: print("There`s no playback running")

def pause_playback(sp):
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

def play_music(sp, uri):
    sp.start_playback(uris=[uri])

def play_playlist(sp, uri):
    sp.start_playback(context_uri=uri)

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

def complex_play_playlist(sp, playlist_name):
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

