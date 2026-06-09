
# state.py

# ============================================
# GLOBAL APPLICATION STATE
# ============================================
#
# Responsibility:
#
#     Maintain shared runtime state for
#     the AI Voice Music System.
#
# This module DOES:
#
#     - track playback mode
#     - store search history
#     - maintain playlist progress
#     - preserve current song information
#     - coordinate playback state
#     - synchronize microphone behavior
#
# This module DOES NOT:
#
#     - perform business logic
#     - play music
#     - search YouTube
#     - control LEDs
#
# Design Principle:
#
#     This module acts as the single
#     source of truth for application
#     runtime state.
#
# Design Flow:
#
#     User Commands
#            ↓
#         main.py
#            ↓
#         state.py
#            ↓
#    Other Functional Modules
#
# ============================================


# ============================================
# PLAYBACK MODE
# ============================================
#
# Current playback context.
#
# Possible values:
#
#     "SEARCH"
#     "PLAYLIST"
#
# Determines how commands such as
# NEXT should behave.
#
# SEARCH mode:
#
#     NEXT
#         ↓
#     Next search result
#
# PLAYLIST mode:
#
#     NEXT
#         ↓
#     Next playlist item
#
# ============================================

play_mode = None


# ============================================
# SEARCH STATE
# ============================================
#
# Preserve search context generated
# from the most recent SEARCH command.
#
# last_query:
#     Original search request.
#
# search_results:
#     Retrieved candidate songs.
#
# search_index:
#     Currently selected search result.
#
# ============================================

last_query = ""

search_results = []

search_index = 0


# ============================================
# PLAYLIST STATE
# ============================================
#
# Maintain playlist playback progress.
#
# playlist:
#     Cached playlist entries.
#
# playlist_index:
#     Current playlist position.
#
# ============================================

playlist = []

playlist_index = 0


# ============================================
# CURRENT SONG
# ============================================
#
# Metadata for the actively selected
# song.
#
# current_song:
#     Display title.
#
# current_url:
#     Original source URL.
#
# Used by:
#
#     SAVE
#     DELETE SONG
#
# operations.
#
# ============================================

current_song = None

current_url = None


# ============================================
# PLAYER
# ============================================
#
# Shared mpv player instance.
#
# Used by playback control functions
# and interrupt mechanisms.
#
# Example:
#
#     STOP
#         ↓
#     player.stop()
#
# ============================================

player = None


# ============================================
# PLAYBACK STATE
# ============================================
#
# is_stopped:
#
#     Interrupt flag indicating that
#     playback should terminate.
#
#
# music_playing:
#
#     Indicates whether audio is
#     currently active.
#
#
# led_running:
#
#     Indicates whether LED
#     visualization should continue.
#
#
# These flags coordinate behavior
# across multiple threads.
#
# Example:
#
#     Switch Press
#            ↓
#      is_stopped
#            ↓
#      player.stop()
#            ↓
#      led_running=False
#
# ============================================

is_stopped = False

music_playing = False

led_running = False


# ============================================
# MICROPHONE STATE
# ============================================
#
# Controls whether the voice assistant
# should reopen the microphone and
# accept new commands.
#
# Example:
#
#     Song Ends
#           ↓
#     listen_requested = True
#           ↓
#       Speak now...
#
# ============================================

listen_requested = True
