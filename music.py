import os

# ========================================
# VERY IMPORTANT:
# make sure Python can find libmpv
# ========================================

os.environ["PATH"] = (
    os.path.dirname(__file__)
    + os.pathsep
    + os.environ["PATH"]
)

import mpv


# ========================================
# CREATE PLAYER
# ========================================

def create_player():

    return mpv.MPV(

        video=False,

        ao="wasapi",

        audio_buffer=2.0,

        cache=True,

        cache_secs=120,

        demuxer_readahead_secs=120
    )


# ========================================
# PLAY
# ========================================

def play(player, filepath):

    player.play(filepath)

    # ====================================
    # BLOCK UNTIL FINISHED
    # ====================================

    player.wait_for_playback()


# ========================================
# STOP
# ========================================

def stop(player):

    if player:

        player.stop()