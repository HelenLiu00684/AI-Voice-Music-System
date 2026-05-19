# music.py

import os

# ============================================
# MPV LIBRARY PATH
# ============================================
#
# Ensure Python can locate libmpv-2.dll
# in the local project directory.
#
# This allows the project to run without
# system-wide mpv installation.
#
# ============================================

os.environ["PATH"] = (

    os.path.dirname(__file__)

    + os.pathsep

    + os.environ["PATH"]
)

import mpv


# ============================================
# CREATE AUDIO PLAYER
# ============================================

def create_player():

    """
    Create and configure the global mpv player.

    Current backend:
        Windows WASAPI

    Future Raspberry Pi migration:
        ao="alsa"
        ao="pulse"
    """

    return mpv.MPV(

        # audio-only playback
        video=False,

        # Windows audio backend
        ao="wasapi",

        # audio buffering
        audio_buffer=2.0,

        # enable caching
        cache=True,

        # cache duration
        cache_secs=120,

        # pre-buffering
        demuxer_readahead_secs=120
    )


# ============================================
# PLAY AUDIO FILE
# ============================================

def play(player, filepath):

    """
    Play a local audio file.

    wait_for_playback() is critical because
    the main system uses playback completion
    to trigger:

    - LED stop
    - microphone reopen
    - next system state transition
    """
    # MPV function,play music 
    player.play(filepath)

    # MPV function,block until playback finishes，python threading synchronization
    player.wait_for_playback()


# ============================================
# STOP PLAYBACK
# ============================================

def stop(player):

    """
    Stop current playback immediately.
    """

    if player:

        player.stop()