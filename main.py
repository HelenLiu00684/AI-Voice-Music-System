# main.py

import threading
import yt_dlp
import os
import state
import serial
import time

from voice import listen
from semantic_ai import analyze_text
from query_builder import build_query
from ai_query import search
from music import create_player, play
from rhythm import analyze_energy
from led_engine import drive_led


# ============================================
# GLOBAL STATE
# ============================================

state.playlist = []
state.current_index = 0

state.is_stopped = False

state.music_playing = False

# IMPORTANT
# controls when microphone should open

state.listen_requested = True


# ============================================
# SERIAL
# ============================================

ser = None


# ============================================
# DOWNLOAD AUDIO
# ============================================

def download_audio(title):

    os.makedirs("temp", exist_ok=True)

    ydl_opts = {

        "format": "bestaudio",

        "outtmpl": "temp/%(id)s.%(ext)s",

        "quiet": True,

        "noplaylist": True,

        "default_search": "ytsearch1",

        "ignoreerrors": True
    }

    try:

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:

            info = ydl.extract_info(title, download=True)

            if not info:
                return None

            if "entries" in info:
                entry = info["entries"][0]
            else:
                entry = info

            filepath = ydl.prepare_filename(entry)

            return filepath

    except Exception as e:

        print("\nDownload failed")
        print(e)

        return None


# ============================================
# LED HELPERS
# ============================================

def led_music_start():

    global ser

    if ser:

        ser.write(b'M')


def led_music_stop():

    global ser

    if ser:

        ser.write(b'S')


# ============================================
# SERIAL LISTENER THREAD
# ============================================

def serial_listener():

    global ser

    while True:

        try:

            if ser.in_waiting:

                line = ser.readline().decode().strip()

                print("\n[ARDUINO EVENT]")
                print(line)

                # ====================================
                # BUTTON INTERRUPT
                # ====================================

                if line == "MIC":

                    print("\nMIC INTERRUPT")

                    # stop everything

                    state.is_stopped = True

                    state.music_playing = False

                    led_music_stop()

                    state.player.stop()

                    # request microphone

                    state.listen_requested = True

        except Exception as e:

            print("\nSerial listener error")
            print(e)


# ============================================
# PLAY SONG
# ============================================

def play_song(title):

    print("\nNow Playing:")
    print(title)

    filepath = download_audio(title)

    if not filepath:

        print("\nDownload failed")

        state.listen_requested = True

        return

    if state.is_stopped:

        print("\nPlayback cancelled")

        state.listen_requested = True

        return

    # ====================================
    # ENTER MUSIC MODE
    # ====================================

    state.music_playing = True

    state.listen_requested = False

    led_music_start()

    # ====================================
    # ANALYZE AUDIO ENERGY
    # ====================================

    energy_list = analyze_energy(filepath)

    # ====================================
    # START LED THREAD
    # ====================================

    threading.Thread(

        target=drive_led,

        args=(energy_list, ser),

        daemon=True

    ).start()

    # ====================================
    # PLAY MUSIC
    # ====================================

    play(state.player, filepath)

    # ====================================
    # MUSIC FINISHED
    # ====================================

    state.music_playing = False

    led_music_stop()

    # reopen microphone automatically

    state.listen_requested = True


# ============================================
# NEXT SONG
# ============================================

def next_song():

    state.current_index += 1

    if state.current_index >= len(state.playlist):

        print("\nNo more songs")

        state.listen_requested = True

        return

    state.is_stopped = False

    state.music_playing = False

    led_music_stop()

    state.player.stop()

    url, title = state.playlist[state.current_index]

    threading.Thread(

        target=play_song,

        args=(title,),

        daemon=True

    ).start()


# ============================================
# MAIN
# ============================================

def main():

    global ser

    print("\n==========================")
    print(" AI Voice Music System ")
    print("==========================\n")

    # ====================================
    # PLAYER
    # ====================================

    state.player = create_player()

    # ====================================
    # SERIAL
    # ====================================

    ser = serial.Serial("COM3", 9600)

    time.sleep(2)

    # ====================================
    # SERIAL THREAD
    # ====================================

    threading.Thread(

        target=serial_listener,

        daemon=True

    ).start()

    # ====================================
    # MAIN LOOP
    # ====================================

    while True:

        # ====================================
        # WAIT FOR LISTEN REQUEST
        # ====================================

        if not state.listen_requested:

            time.sleep(0.1)

            continue

        print("\n🎤 Listening...\n")

        text = listen()

        if not text:

            continue

        print("\nYou said:")
        print(text)

        text = text.lower().strip()

        # microphone request consumed

        state.listen_requested = False

        # ====================================
        # STOP
        # ====================================

        if text == "stop":

            print("\nStopping playback...")

            state.is_stopped = True

            state.music_playing = False

            led_music_stop()

            state.player.stop()

            state.listen_requested = True

            continue

        # ====================================
        # NEXT
        # ====================================

        if text == "next":

            print("\nNext song...")

            next_song()

            continue

        # ====================================
        # NEW MUSIC REQUEST
        # ====================================

        state.is_stopped = False

        state.music_playing = False

        led_music_stop()

        state.player.stop()

        print("\nAI semantic parsing...\n")

        try:

            ai_result = analyze_text(text)

            print(ai_result)

        except Exception as e:

            print("\nAI failed")
            print(e)

            state.listen_requested = True

            continue

        # ====================================
        # BUILD QUERY
        # ====================================

        try:

            query = build_query(ai_result)

            print("\nFinal Query:")
            print(query)

        except Exception as e:

            print("\nQuery build failed")
            print(e)

            state.listen_requested = True

            continue

        # ====================================
        # SEARCH
        # ====================================

        try:

            results = search(query)

        except Exception as e:

            print("\nSearch failed")
            print(e)

            state.listen_requested = True

            continue

        if not results:

            print("\nNo songs found")

            state.listen_requested = True

            continue

        # ====================================
        # SAVE PLAYLIST
        # ====================================

        state.playlist = results

        state.current_index = 0

        # ====================================
        # FIRST SONG
        # ====================================

        url, title = results[0]

        threading.Thread(

            target=play_song,

            args=(title,),

            daemon=True

        ).start()


# ============================================
# START
# ============================================

if __name__ == "__main__":

    main()