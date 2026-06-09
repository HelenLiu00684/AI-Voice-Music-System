
import json
import os


# ============================================
# PLAYLIST PERSISTENCE LAYER
# ============================================
#
# Responsibility:
#
#     Manage persistent playlist storage
#     using a local JSON file.
#
# This module DOES:
#
#     - load playlist data
#     - save playlist data
#     - add songs
#     - delete songs
#     - clear playlists
#
# This module DOES NOT:
#
#     - play music
#     - search YouTube
#     - download audio
#     - perform voice recognition
#
# Design Flow:
#
#     Voice Commands
#             ↓
#      Playlist Service
#             ↓
#       JSON Persistence
#             ↓
#       playlist.json
#
# Design Principle:
#
#     Separate playlist persistence
#     from playback and business logic.
#
# ============================================


# ============================================
# PLAYLIST STORAGE FILE
# ============================================
#
# JSON file used to preserve playlist
# state across application restarts.
#
# ============================================

PLAYLIST_FILE = "playlist.json"


# ============================================
# LOAD JSON FILE
# ============================================

def load_list():

    """
    Load playlist data from persistent storage.

    Returns:

        List of songs:

            [
                {
                    "title": ...,
                    "url": ...
                },
                ...
            ]

    Behavior:

        Returns an empty list if no playlist
        file exists.

    Design Notes:

        Missing playlists are treated as an
        empty playlist rather than an error.
    """

    if not os.path.exists(

        PLAYLIST_FILE

    ):

        return []

    with open(

        PLAYLIST_FILE,

        "r",

        encoding="utf-8"

    ) as f:

        return json.load(f)


# ============================================
# SAVE JSON FILE
# ============================================

def save_list(data):

    """
    Persist playlist data to disk.

    Input:

        data:
            Playlist data to be stored.

    Behavior:

        Overwrites the existing playlist
        with the provided state.

    Design Notes:

        The JSON file is treated as the
        authoritative playlist state.
    """

    with open(

        PLAYLIST_FILE,

        "w",

        encoding="utf-8"

    ) as f:

        json.dump(

            data,

            f,

            indent=2,

            ensure_ascii=False

        )


# ============================================
# ADD SONG
# ============================================

def add_song(

    title,

    url

):

    """
    Add a song to the persistent playlist.

    Input:

        title:
            Song title.

        url:
            Song source URL.

    Behavior:

        Loads the current playlist,
        appends the new song,
        and saves the updated state.

    Design Notes:

        The playlist follows a
        read-modify-write workflow.
    """

    songs = load_list()

    songs.append(

        {

            "title": title,

            "url": url

        }

    )

    save_list(

        songs

    )


# ============================================
# DELETE SONG
# ============================================

def delete_song(

    title

):

    """
    Remove songs matching the specified title.

    Input:

        title:
            Song title to remove.

    Behavior:

        Songs with matching titles are
        filtered out and the updated
        playlist is persisted.

    Design Notes:

        Multiple matching entries will
        be removed.
    """

    songs = load_list()

    songs = [

        s

        for s in songs

        if s["title"] != title

    ]

    save_list(

        songs

    )


# ============================================
# CLEAR PLAYLIST
# ============================================

def clear_list():

    """
    Delete the entire persistent playlist.

    Behavior:

        Removes the playlist JSON file
        from disk.

    Design Notes:

        Clearing the playlist resets the
        playlist state completely.
    """

    if os.path.exists(

        PLAYLIST_FILE

    ):

        os.remove(

            PLAYLIST_FILE

        )

