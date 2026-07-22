import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
    scope="playlist-modify-private playlist-modify-public user-read-private",
    cache_path=".cache",
    show_dialog=True
))
print("CURRENT USER:", sp.current_user())
print("TOKEN SCOPE:", sp.auth_manager.get_cached_token()["scope"])

playlist = sp.current_user_playlist_create(
    name="Fast Driving Playlist",
    public=False
)

print("Playlist created:", playlist["id"])
track_uris = []

with open("songs.txt", "r", encoding="utf-8") as f:
    songs = f.readlines()

for song in songs:
    song = song.strip()

    if not song:
        continue

    if " - " in song:
        artist, track = song.split(" - ", 1)
        query = f'track:{track} artist:{artist}'
    else:
        query = song

    if not query.strip():
        continue

    try:
        results = sp.search(q=query, type="track", limit=1)
        tracks = results["tracks"]["items"]

        if tracks:
            track_uris.append(tracks[0]["uri"])
            print("Found:", tracks[0]["name"])
        else:
            print("Not found:", song)

    except Exception as e:
        print("Search failed for:", song, "| Error:", e)
print("TOTAL TRACKS FOUND:", len(track_uris))

if track_uris:
    for i in range(0, len(track_uris), 100):
        sp.playlist_add_items(
            playlist["id"],
            track_uris[i:i+100]
        )

print("UPLOAD COMPLETE")
print("Playlist created successfully!")
