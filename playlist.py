import json
import os

PLAYLIST_DIR = "playlists"
os.makedirs(PLAYLIST_DIR, exist_ok=True)


def save_playlist(name, songs):
    path = os.path.join(PLAYLIST_DIR, f"{name}.json")

    data = [{"title": title} for _, title in songs]

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def list_playlists():
    return [f.replace(".json", "") for f in os.listdir(PLAYLIST_DIR)]


def load_playlist(name):
    path = os.path.join(PLAYLIST_DIR, f"{name}.json")

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def delete_playlist(name):
    path = os.path.join(PLAYLIST_DIR, f"{name}.json")

    if os.path.exists(path):
        os.remove(path)