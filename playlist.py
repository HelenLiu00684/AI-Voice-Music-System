
import json
import os


PLAYLIST_FILE = "playlist.json"


# ============================================
# LOAD JSON FILE
# ============================================

def load_list():

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

    songs = load_list()

    songs=[

        s

        for s in songs

        if s["title"]!=title

    ]

    save_list(

        songs

    )



# ============================================
# CLEAR PLAYLIST
# ============================================

def clear_list():

    if os.path.exists(

        PLAYLIST_FILE

    ):

        os.remove(

            PLAYLIST_FILE

        )

