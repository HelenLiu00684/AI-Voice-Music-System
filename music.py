
# music.py

# ============================================
# MUSIC PLAYBACK LAYER
# ============================================
#
# Responsibility:
#
#     Provide audio playback services using
#     the mpv backend.
#
# This module DOES:
#
#     - create audio player instances
#     - play local audio files
#     - stop playback
#
# This module DOES NOT:
#
#     - search music
#     - download audio
#     - perform voice recognition
#     - drive LED visualization
#
# Design Flow:
#
#     Local Audio File
#             ↓
#         mpv Player
#             ↓
#       Audio Backend
#             ↓
#        Speaker Output
#
# ============================================

import os
import time

# ============================================
# MPV LIBRARY PATH
# ============================================
#
# Ensure Python can locate libmpv-2.dll
# in the local project directory.
#
# This allows the project to run without
# requiring a system-wide mpv installation.
#
# Improve project portability by bundling
# mpv dependencies with the application.
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
    Create and configure an mpv player instance.

    Current Platform:
        Windows

    Audio Backend:
        WASAPI

    Future Raspberry Pi Migration:
        ALSA
        PulseAudio

    Returns:
        Configured mpv player object.

    Design Notes:

        Player configuration is centralized
        to simplify future backend migration.
    """

    # ====================================
    # PLAYBACK CONFIGURATION
    # ====================================
    #
    # Configure buffering and caching to
    # improve playback stability and reduce
    # interruptions caused by I/O delays.
    #
    # ====================================

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

    Input:

        player:
            Configured mpv player instance.

        filepath:
            Local audio file path.

    Behavior:

        Blocking playback.

    The function returns only when:

        - playback completes, or
        - playback is interrupted externally.

    Design Notes:

        The blocking behavior allows the
        main state machine to synchronize
        playback state transitions.
    
    Note:

        I used the python-mpv library.

        The MPV player provides a built-in
        wait_for_playback() method, which blocks
        the current workflow until playback
        finishes or is interrupted by stop().

        This mechanism was integrated into the
        main state machine to synchronize voice
        control and music playback.
    """

    player.play(filepath)

    player.wait_for_playback()


# ============================================
# STOP PLAYBACK
# ============================================

def stop(player):

    """
    Stop current playback immediately.

    Input:

        player:
            Configured mpv player instance.

    Behavior:

        Immediately terminates active playback.

    Design Notes:

        Primarily used by the interrupt
        mechanism to regain control of the
        voice assistant workflow.

    Example:

            Switch Press
                   ↓
              player.stop()
                   ↓
            Playback Ends
                   ↓
             Reopen Microphone
    """

    if player:

        player.stop()

