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



# def play_song(title, ser):

#     print("\nNow Playing:")
#     print(title)

#     # ==========================
#     # download audio
#     # ==========================

#     filepath = download_audio(
#         title
#     )
#     print("DOWNLOAD OK")
#     if not filepath:

#         print(
#             "\nDownload failed"
#         )

#         return

#     # ==========================
#     # analyze energy
#     # ==========================

#     energy_list = analyze_energy(
#         filepath
#     )

#     print("ENERGY ANALYSIS OK")

#     print(
#         "ENERGY COUNT:",
#         len(energy_list)
#     )
#     # ==========================
#     # start LED thread
#     # ==========================
#     print("START LED THREAD")

#     state.led_running = True

#     led_thread = threading.Thread(

#         target=drive_led,

#         args=(
#             energy_list,
#             ser
#         )

#     )

#     led_thread.start()

#     # ==========================
#     # notify Arduino
#     # ==========================

#     ser.write(
#         b'M'
#     )

#     # ==========================
#     # blocking playback
#     # returns when:
#     #
#     # 1 natural finish
#     # 2 player.stop()
#     #
#     # ==========================

#     play(

#         state.player,

#         filepath

#     )

#     # ==========================
#     # cleanup
#     # ==========================

#     ser.write(
#         b'S'
#     )

#     time.sleep(
#         0.2
#     )

#     print(
#         "\nMusic finished"
#     )




def play_song(title, ser):

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

    state.led_running=True

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

    # cleanup

    state.led_running=False

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


# def serial_listener(ser):

#     while True:

#         try:

#             line=(

#                 ser.readline()

#                 .decode()

#                 .strip()

#             )

#             if line=="MIC":

#                 print(
#                     "\nMIC interrupt received"
#                 )

#                 # immediately stop playback

#                 stop(
#                     state.player
#                 )

#                 # request microphone reopen

#                 if not state.listen_requested:

#                     state.listen_requested=True


#         except Exception as e:

#             print(
#                 "\nSerial listener error"
#             )

#             print(e)


def serial_listener(ser):

    while True:

        try:

            line=(

                ser.readline()

                .decode()

                .strip()

            )

            if line=="MIC":

                print(
                    "\nMIC interrupt received"
                )

                # stop LED immediately

                state.led_running=False

                # stop music

                stop(
                    state.player
                )

                if not state.listen_requested:

                    state.listen_requested=True


        except Exception as e:

            print(
                "\nSerial listener error"
            )

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

        115200
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

        state.listen_requested=False

        state.is_stopped=False


        # ====================================
        # MICROPHONE
        # ====================================

        print(
            "\n🎤 Listening...\n"
        )

        try:

            text=listen()

        except Exception:

            print(
                "\nListen timeout"
            )

            state.listen_requested=True

            continue


        if not text:

            state.listen_requested=True

            continue


        print(
            "You said:"
        )

        print(
            text
        )


        # ====================================
        # COMMAND PARSER
        # ====================================

        cmd,arg=(

            parse_command(
                text
            )

        )

        print(

            "\nCOMMAND:",

            cmd

        )


        # ====================================
        # SAVE
        # ====================================

        if cmd=="SAVE":

            if state.current_song:

                add_song(

                    state.current_song,

                    state.current_url

                )

                print(
                    "\nSong saved"
                )

            state.listen_requested=True

            continue


        # ====================================
        # PLAY LIST
        # ====================================

        if cmd=="PLAYLIST":

            songs=load_list()

            if not songs:

                print(
                    "\nPlaylist empty"
                )

                state.listen_requested=True

                continue

            state.play_mode="PLAYLIST"

            state.playlist=songs

            state.playlist_index=0

            song=songs[0]

            state.current_song=(

                song["title"]

            )

            state.current_url=(

                song["url"]

            )

            play_song(

                state.current_song,

                ser

            )

            state.listen_requested=True

            continue


        # ====================================
        # DELETE SONG
        # ====================================

        if cmd=="DELETE_SONG":

            if state.current_song:

                delete_song(

                    state.current_song

                )

                print(
                    "\nSong deleted"
                )

            state.listen_requested=True

            continue


        # ====================================
        # DELETE LIST
        # ====================================

        if cmd=="DELETE_LIST":

            clear_list()

            print(
                "\nPlaylist deleted"
            )

            state.listen_requested=True

            continue


        # ====================================
        # NEXT
        # ====================================

        if cmd=="NEXT":

            if state.play_mode=="PLAYLIST":

                state.playlist_index+=1

                if (

                    state.playlist_index

                    >=

                    len(

                        state.playlist

                    )

                ):

                    print(
                        "\nPlaylist finished"
                    )

                    state.listen_requested=True

                    continue

                song=(

                    state.playlist[

                        state.playlist_index

                    ]

                )

                state.current_song=(

                    song["title"]

                )

                state.current_url=(

                    song["url"]

                )

                play_song(

                    state.current_song,

                    ser

                )

                state.listen_requested=True

                continue


            if state.play_mode=="SEARCH":

                state.search_index+=1

                if (

                    state.search_index

                    >=

                    len(

                        state.search_results

                    )

                ):

                    print(
                        "\nSearching more..."
                    )

                    state.search_results=(

                        search(

                            state.last_query

                        )

                    )

                    state.search_index=0

                    if not state.search_results:

                        state.listen_requested=True

                        continue


                url,title=(

                    state.search_results[

                        state.search_index

                    ]

                )

                state.current_song=title

                state.current_url=url

                play_song(

                    title,

                    ser

                )

                state.listen_requested=True

                continue


            print(
                "\nNothing to skip"
            )

            state.listen_requested=True

            continue


        # ====================================
        # BUILD QUERY
        # ====================================

        if cmd=="SEARCH":

            query=arg

        else:

            print(
                "\nAI semantic parsing...\n"
            )

            ai_result=(

                analyze_text(
                    text
                )

            )

            if not ai_result:

                state.listen_requested=True

                continue

            query=(

                build_query(
                    ai_result
                )

            )


        # ====================================
        # SEARCH
        # ====================================

        results=(

            search(
                query
            )

        )

        if not results:

            state.listen_requested=True

            continue


        state.play_mode="SEARCH"

        state.search_results=results

        state.search_index=0

        state.last_query=query


        url,title=(

            results[0]

        )

        state.current_song=title

        state.current_url=url


        play_song(

            title,

            ser

        )

        state.listen_requested=True



# ============================================
# SYSTEM ENTRY
# ============================================

if __name__ == "__main__":

    main()