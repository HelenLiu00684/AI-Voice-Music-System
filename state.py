# state.py

# ============================================
# PLAYLIST STATE
# ============================================

# List of search results:
#
# [
#   (url, title),
#   ...
# ]
#
playlist = []

# Current index inside playlist
current_index = 0


# ============================================
# GLOBAL AUDIO PLAYER
# ============================================

# Shared mpv player instance
player = None


# ============================================
# PLAYBACK STATE
# ============================================

# True when playback is manually stopped
is_stopped = False

# True while music is actively playing
music_playing = False


# ============================================
# MICROPHONE CONTROL
# ============================================
#
# Controls when voice listening
# is allowed to start.
#
# True:
#     microphone listening enabled
#
# False:
#     listening disabled during playback
#
listen_requested = True