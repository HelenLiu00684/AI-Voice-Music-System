# main.py

import os
import time
import serial
import threading
import yt_dlp

import state

serial_lock = threading.Lock()

from voice import listen
from command_parser import parse_command

from playlist import (
    add_song,
    load_list,
    delete_song,
    clear_list
)

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

def download_audio(title):

    """
    Download audio-only content from YouTube.

    Input:
        title:
            Song title or YouTube search text.

    Output:
        filepath:
            Local downloaded audio file path.

        None:
            Returned if download fails.
    """

    os.makedirs("temp", exist_ok=True)

    ydl_opts = {
        "format": "bestaudio[ext=m4a]/bestaudio",
        "outtmpl": "temp/%(id)s.%(ext)s",
        "quiet": True,
        "noplaylist": True,
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

def play_song(title, ser):

    """
    Full playback pipeline.

    Input:
        title:
            Song title selected from search
            results or playlist.

        ser:
            Active serial connection to Arduino.

    Processing Flow:
        title
          ↓
        download audio
          ↓
        analyze audio energy
          ↓
        start LED thread
          ↓
        notify Arduino music started
          ↓
        play music
          ↓
        cleanup LED / Arduino state

    Output:
        No return value.

    Design Notes:
        This function blocks during playback.
        It returns when the song naturally
        finishes or playback is interrupted.
    """

    print("\nNow Playing:")
    print(title)

    filepath = download_audio(
        title
    )

    print("DOWNLOAD OK")

    if not filepath:

        return

    energy_list = analyze_energy(
        filepath
    )

    print("ENERGY ANALYSIS OK")

    print(
        "ENERGY COUNT:",
        len(energy_list)
    )

    print("START LED THREAD")

    state.led_running = True

    led_thread = threading.Thread(

        target=drive_led,

        args=(
            energy_list,
            ser,
            serial_lock
        )
    )

    led_thread.start()

    with serial_lock:

        ser.write(
            b'M'
        )

    play(
        state.player,
        filepath
    )

    state.led_running = False

    with serial_lock:

        ser.write(
            b'S'
        )

    time.sleep(
        0.2
    )

    print(
        "\nMusic finished"
    )


# ============================================
# SERIAL LISTENER
# ============================================

def serial_listener(ser):

    """
    Listen for Arduino serial events.

    Input:
        ser:
            Active serial connection.

    Expected Arduino Input:
        "MIC"

    Behavior:
        When MIC is received:

            stop LED
              ↓
            stop playback
              ↓
            request microphone reopen

    Output:
        No return value.

    Design Notes:
        This function runs in a daemon
        thread and listens continuously.
    """

    while True:

        try:

            line = (
                ser.readline()
                .decode()
                .strip()
            )

            if line == "MIC":

                print(
                    "\nMIC interrupt received"
                )

                state.led_running = False

                stop(
                    state.player
                )

                if not state.listen_requested:

                    state.listen_requested = True

        except Exception as e:

            print(
                "\nSerial listener error"
            )

            print(e)


# ============================================
# MAIN SYSTEM LOOP
# ============================================

def main():

    """
    Main event-driven state machine.

    Responsibilities:
        - initialize player
        - open serial connection
        - start serial listener thread
        - capture voice commands
        - dispatch command actions
        - manage playlist/search modes
        - run AI semantic search
        - coordinate playback and LED state

    Main Flow:
        Voice Input
            ↓
        Command Parser
            ↓
        Command Dispatch
            ↓
        State Update
            ↓
        Functional Modules

    Output:
        No return value.
    """

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
        115200
    )

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
        # MICROPHONE INPUT
        # ====================================

        print(
            "\n🎤 Listening...\n"
        )

        try:

            text = listen()

        except Exception:

            print(
                "\nListen timeout"
            )

            state.listen_requested = True

            continue

        if not text:

            state.listen_requested = True

            continue

        print("You said:")
        print(text)

        # ====================================
        # COMMAND PARSER
        # ====================================
        #
        # Input:
        #     text:
        #         Raw recognized speech.
        #
        # Output:
        #     cmd:
        #         Normalized command type.
        #
        #     arg:
        #         Optional command argument.
        #
        # Example:
        #
        #     "search Taylor Swift"
        #
        #         ↓
        #
        #     cmd = "SEARCH"
        #     arg = "Taylor Swift"
        #
        # ====================================

        cmd, arg = parse_command(
            text
        )

        print(
            "\nCOMMAND:",
            cmd
        )

        # ====================================
        # SAVE CURRENT SONG
        # ====================================

        if cmd == "SAVE":

            if state.current_song:

                add_song(
                    state.current_song,
                    state.current_url
                )

                print(
                    "\nSong saved"
                )

            state.listen_requested = True

            continue

        # ====================================
        # PLAY PLAYLIST
        # ====================================

        if cmd == "PLAYLIST":

            songs = load_list()

            if not songs:

                print(
                    "\nPlaylist empty"
                )

                state.listen_requested = True

                continue

            state.play_mode = "PLAYLIST"
            state.playlist = songs
            state.playlist_index = 0

            song = songs[0]

            state.current_song = song["title"]
            state.current_url = song["url"]

            play_song(
                state.current_song,
                ser
            )

            state.listen_requested = True

            continue

        # ====================================
        # DELETE CURRENT SONG
        # ====================================

        if cmd == "DELETE_SONG":

            if state.current_song:

                delete_song(
                    state.current_song
                )

                print(
                    "\nSong deleted"
                )

            state.listen_requested = True

            continue

        # ====================================
        # DELETE ENTIRE PLAYLIST
        # ====================================

        if cmd == "DELETE_LIST":

            clear_list()

            print(
                "\nPlaylist deleted"
            )

            state.listen_requested = True

            continue

        # ====================================
        # STOP PLAYBACK
        # ====================================

        if cmd == "STOP":

            state.led_running = False

            stop(
                state.player
            )

            print(
                "\nPlayback stopped"
            )

            state.listen_requested = True

            continue

        # ====================================
        # UNKNOWN COMMAND
        # ====================================

        if cmd == "UNKNOWN":

            print(
                "\nUnknown command"
            )

            state.listen_requested = True

            continue

        # ====================================
        # NEXT SONG
        # ====================================

        if cmd == "NEXT":

            # -------------------------
            # PLAYLIST MODE
            # -------------------------

            if state.play_mode == "PLAYLIST":

                state.playlist_index += 1

                if (
                    state.playlist_index
                    >=
                    len(state.playlist)
                ):

                    print(
                        "\nPlaylist finished"
                    )

                    state.listen_requested = True

                    continue

                song = state.playlist[
                    state.playlist_index
                ]

                state.current_song = song["title"]
                state.current_url = song["url"]

                play_song(
                    state.current_song,
                    ser
                )

                state.listen_requested = True

                continue

            # -------------------------
            # SEARCH MODE
            # -------------------------

            if state.play_mode == "SEARCH":

                state.search_index += 1

                if (
                    state.search_index
                    >=
                    len(state.search_results)
                ):

                    print(
                        "\nSearching more..."
                    )

                    state.search_results = search(
                        state.last_query
                    )

                    state.search_index = 0

                    if not state.search_results:

                        state.listen_requested = True

                        continue

                url, title = state.search_results[
                    state.search_index
                ]

                state.current_song = title
                state.current_url = url

                play_song(
                    title,
                    ser
                )

                state.listen_requested = True

                continue

            print(
                "\nNothing to skip"
            )

            state.listen_requested = True

            continue

        # ====================================
        # AI SEMANTIC SEARCH
        # ====================================
        #
        # Input:
        #     arg:
        #         Raw search request extracted
        #         by the command parser.
        #
        # Examples:
        #     search Taylor Swift
        #     search FIFA 2026
        #     search the Shakira FIFA song
        #
        # Processing Flow:
        #     Raw Query
        #          ↓
        #     Semantic AI
        #          ↓
        #     Structured JSON
        #          ↓
        #     Query Builder
        #          ↓
        #     Optimized Search Query
        #          ↓
        #     YouTube Search
        #
        # Output:
        #     query:
        #         Final optimized keyword
        #         string used for retrieval.
        #
        # ====================================

        if cmd == "SEARCH":

            print(
                "\nAI semantic parsing...\n"
            )

            print(
                "Original Query:"
            )

            print(
                arg
            )

            ai_result = analyze_text(
                arg
            )

            if not ai_result:

                print(
                    "\nSemantic parsing failed"
                )

                state.listen_requested = True

                continue

            print(
                "\nAI Semantic Result:"
            )

            print(
                ai_result
            )

            query = build_query(
                ai_result
            )

            print(
                "\nOptimized Search Query:"
            )

            print(
                query
            )

        else:

            state.listen_requested = True

            continue

        # ====================================
        # YOUTUBE SEARCH
        # ====================================
        #
        # Input:
        #     query:
        #         Optimized keyword string.
        #
        # Output:
        #     results:
        #         [
        #             (
        #                 url,
        #                 title
        #             ),
        #             ...
        #         ]
        #
        # ====================================

        results = search(
            query
        )

        if not results:

            print(
                "\nNo search results found."
            )

            state.listen_requested = True

            continue

        # ====================================
        # STORE SEARCH STATE
        # ====================================

        state.play_mode = "SEARCH"
        state.search_results = results
        state.search_index = 0
        state.last_query = query

        # ====================================
        # SELECT FIRST SEARCH RESULT
        # ====================================

        url, title = results[0]

        state.current_song = title
        state.current_url = url

        # ====================================
        # PLAY SELECTED SONG
        # ====================================

        play_song(
            title,
            ser
        )

        state.listen_requested = True


# ============================================
# SYSTEM ENTRY
# ============================================

if __name__ == "__main__":

    main()