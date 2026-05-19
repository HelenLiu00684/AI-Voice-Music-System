# state.py

playlist = []          # [(None, title)]
current_index = 0

player = None

# cache: index -> filepath
cache = {}

mode = "INPUT"
pending_save = False
is_stopped = False
music_playing = False