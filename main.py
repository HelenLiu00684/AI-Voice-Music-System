# main.py

import os
import time
import serial
import threading
import yt_dlp

import state

from voice import listen

from semantic_ai import analyze_text

from query_builder import build_query

from ai_query import search

from rhythm import analyze_energy

from led_engine import drive_led

from music import (
    create_player,
    play,
    stop
)


# ============================================
# DOWNLOAD AUDIO
# ============================================
#
# Download audio-only content from YouTube.
#
# Audio files are temporarily stored inside:
#
#     temp/
#
# ============================================

def download_audio(title):

    os.makedirs("temp", exist_ok=True)

    ydl_opts = {

        # audio only
        "format": "bestaudio[ext=m4a]/bestaudio",

        # output filename
        "outtmpl": "temp/%(id)s.%(ext)s",

        # reduce console spam
        "quiet": True,

        # avoid playlist extraction
        "noplaylist": True,

        # search only first result
        "default_search": "ytsearch1"
    }

    try:

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:

            info = ydl.extract_info(

                title,

                download=True
            )

            entry = info["entries"][0]

            filepath = ydl.prepare_filename(entry)

            return filepath

    except Exception as e:

        print("\nDownload failed")

        print(e)

        return None


# ============================================
# PLAY SONG
# ============================================
#
# Full playback pipeline:
#
# download
#     →
# analyze energy
#     →
# start LED thread
#     →
# play music
#
# ============================================

def play_song(title, ser):

    print("\nNow Playing:")
    print(title)

    # ====================================
    # DOWNLOAD AUDIO
    # ====================================

    filepath = download_audio(title)

    if not filepath:

        print("\nDownload failed")

        return

    # ====================================
    # PLAYBACK CANCEL CHECK
    # ====================================

    if state.is_stopped:

        print("\nPlayback cancelled")

        return

    # ====================================
    # ANALYZE AUDIO ENERGY
    # ====================================

    energy_list = analyze_energy(filepath)

    # ====================================
    # ENABLE MUSIC STATE
    # ====================================

    state.music_playing = True

    # ====================================
    # START LED REACTIVE THREAD
    # ====================================

    threading.Thread(

        target=drive_led,

        args=(energy_list, ser),

        daemon=True

    ).start()

    # ====================================
    # NOTIFY ARDUINO
    # ====================================

    ser.write(b'M')

    # ====================================
    # PLAY AUDIO
    # ====================================

    play(state.player, filepath)

    # ====================================
    # MUSIC FINISHED
    # ====================================

    state.music_playing = False

    ser.write(b'S')

    print("\nMusic finished")


# ============================================
# SERIAL LISTENER
# ============================================
#
# Listen for Arduino interrupt events.
#
# Example:
#
# MIC
#     →
# stop playback
#     →
# reopen microphone
#
# ============================================

def serial_listener(ser):

    while True:

        try:

            line = (

                ser.readline()

                .decode()

                .strip()
            )

            if line == "MIC":

                print("\nMIC interrupt received")

                # stop playback
                state.music_playing = False

                state.is_stopped = True

                stop(state.player)

                # reopen listening
                state.listen_requested = True

        except Exception as e:

            print("\nSerial listener error")

            print(e)


# ============================================
# MAIN SYSTEM LOOP
# ============================================

def main():

    print("\n==========================")
    print(" AI Voice Music System ")
    print("==========================\n")

    # ====================================
    # CREATE AUDIO PLAYER
    # ====================================

    state.player = create_player()

    # ====================================
    # OPEN SERIAL PORT
    # ====================================

    ser = serial.Serial(

        "COM3",

        9600
    )

    # allow Arduino reset
    time.sleep(2)

    # ====================================
    # START SERIAL THREAD
    # ====================================

    threading.Thread(

        target=serial_listener,

        args=(ser,),

        daemon=True

    ).start()

    # ====================================
    # MAIN EVENT LOOP
    # ====================================

    while True:

        # ====================================
        # WAIT FOR LISTEN REQUEST
        # ====================================

        if not state.listen_requested:

            time.sleep(0.1)

            continue

        # ====================================
        # RESET STATES
        # ====================================

        state.listen_requested = False

        state.is_stopped = False

        # ====================================
        # START MICROPHONE
        # ====================================

        print("\n🎤 Listening...\n")

        text = listen()

        if not text:

            print("\nNo speech detected")

            state.listen_requested = True

            continue

        print("You said:")

        print(text)

        # ====================================
        # AI SEMANTIC ANALYSIS
        # ====================================

        print("\nAI semantic parsing...\n")

        ai_result = analyze_text(text)

        if not ai_result:

            state.listen_requested = True

            continue

        # ====================================
        # BUILD SEARCH QUERY
        # ====================================

        query = build_query(ai_result)

        print("\nFinal Query:")

        print(query)

        # ====================================
        # SEARCH YOUTUBE
        # ====================================

        results = search(query)

        if not results:

            print("\nNo songs found")

            state.listen_requested = True

            continue

        # ====================================
        # STORE PLAYLIST
        # ====================================

        state.playlist = results

        state.current_index = 0

        # ====================================
        # SELECT FIRST RESULT
        # ====================================

        _, title = results[0]

        # ====================================
        # PLAY SONG
        # ====================================

        play_song(title, ser)

        # ====================================
        # REOPEN MICROPHONE
        # ====================================

        state.listen_requested = True


# ============================================
# SYSTEM ENTRY
# ============================================

if __name__ == "__main__":

    main()