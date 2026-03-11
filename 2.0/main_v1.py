#Testing and developing the spotify integration

#packages
import spotipy
import subprocess
from spotipy.oauth2 import SpotifyOAuth

#auth
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="f4dbb04636f34cd183867be4aa645af4",
    client_secret="fa271815bd414006a69636ea96813bfe",
    redirect_uri="http://127.0.0.1:8888/callback",
    scope = "user-modify-playback-state user-read-playback-state user-library-read playlist-read-private"
))

#basic commands

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

#main area

while True:
    usr_input = str(input("Please type your command: "))

    if "search" in usr_input:
        search_for = str(input("Music name: "))
        search_results = music_search(sp, search_for)
        print("Results:\n")
        for key,value in search_results.items():
            print(f"{key} -> Name: {value["track"]}| URI: {value["uri"]}")

