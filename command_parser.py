
# ============================================
# VOICE COMMAND PARSER
# ============================================
#
# SUPPORTED VOICE COMMANDS
#
# ------------------------------------------------
# Search Music
# ------------------------------------------------
#
# Examples:
#
#     search Taylor Swift
#     search Adele
#     search Titanic soundtrack
#
# Optional Shortcut:
#
#     one Taylor Swift
#
# Returns:
#
#     ("SEARCH", query)
#
#
# ------------------------------------------------
# Save Current Song
# ------------------------------------------------
#
# Examples:
#
#     save
#     save song
#     save this song
#     save into the playlist
#     write into the playlist
#
# Optional Shortcut:
#
#     two
#
# Returns:
#
#     ("SAVE", None)
#
#
# ------------------------------------------------
# Play Next Song
# ------------------------------------------------
#
# Examples:
#
#     next
#     next song
#     play next song
#
# Optional Shortcut:
#
#     three
#
# Returns:
#
#     ("NEXT", None)
#
#
# ------------------------------------------------
# Play Playlist
# ------------------------------------------------
#
# Examples:
#
#     play list
#     play playlist
#     play my playlist
#
# Optional Shortcut:
#
#     four
#
# Returns:
#
#     ("PLAYLIST", None)
#
#
# ------------------------------------------------
# Delete Current Song
# ------------------------------------------------
#
# Examples:
#
#     delete song
#     remove this song
#
# Optional Shortcut:
#
#     five
#
# Returns:
#
#     ("DELETE_SONG", None)
#
#
# ------------------------------------------------
# Delete Entire Playlist
# ------------------------------------------------
#
# Examples:
#
#     delete playlist
#     clear playlist
#
# Optional Shortcut:
#
#     six
#
# Returns:
#
#     ("DELETE_LIST", None)
#
#
# ------------------------------------------------
# Stop Playback
# ------------------------------------------------
#
# Examples:
#
#     stop music
#     stop song
#
# Optional Shortcut:
#
#     seven
#
# Returns:
#
#     ("STOP", None)
#
#
# ------------------------------------------------
# Unsupported Input
# ------------------------------------------------
#
# Any input that does not match the
# commands above is classified as:
#
#     ("UNKNOWN", text)
#
# Examples:
#
#     hello
#     good morning
#     abcxyz
#
#
# ============================================
# RESPONSIBILITY
# ============================================
#
# Convert raw speech recognition output
# into normalized commands consumed by
# the main state machine.
#
# Design Flow:
#
#     Speech Recognition
#             ↓
#      Command Parser
#             ↓
#     Normalized Events
#             ↓
#      Main State Machine
#
# Design Principle:
#
#     Explicit commands improve system
#     reliability and avoid unintended
#     actions caused by speech recognition
#     ambiguity.
#
# ============================================


def parse_command(text):

    """
    Parse voice input into normalized commands.

    Input:
        Raw speech recognition text.

    Output:
        (
            command,
            argument
        )

    Examples:

        "search Taylor Swift"

            →

        ("SEARCH", "Taylor Swift")


        "save song"

            →

        ("SAVE", None)


        "next song"

            →

        ("NEXT", None)


        "hello"

            →

        ("UNKNOWN", "hello")
    """

    text = text.lower().strip()


    # ====================================
    # SEARCH COMMAND
    # ====================================

    if text.startswith(

        ("search ", "one ")

    ):

        if text.startswith(

            "search "

        ):

            query = text.replace(

                "search",

                "",

                1

            )

        else:

            query = text.replace(

                "one",

                "",

                1

            )

        query = query.strip()

        return (

            "SEARCH",

            query

        )


    # ====================================
    # SAVE CURRENT SONG
    # ====================================

    if text in [

        "save",

        "save song",

        "save this song",

        "save into the playlist",

        "write into the playlist",

        "two"

    ]:

        return (

            "SAVE",

            None

        )


    # ====================================
    # NEXT SONG
    # ====================================

    if text in [

        "next",

        "next song",

        "play next song",

        "three"

    ]:

        return (

            "NEXT",

            None

        )


    # ====================================
    # PLAY PLAYLIST
    # ====================================

    if text in [

        "play list",

        "play playlist",

        "play my playlist",

        "four"

    ]:

        return (

            "PLAYLIST",

            None

        )


    # ====================================
    # DELETE CURRENT SONG
    # ====================================

    if text in [

        "delete song",

        "remove this song",

        "five"

    ]:

        return (

            "DELETE_SONG",

            None

        )


    # ====================================
    # DELETE ENTIRE PLAYLIST
    # ====================================

    if text in [

        "delete playlist",

        "clear playlist",

        "six"

    ]:

        return (

            "DELETE_LIST",

            None

        )


    # ====================================
    # STOP PLAYBACK
    # ====================================

    if text in [

        "stop music",

        "stop song",

        "seven"

    ]:

        return (

            "STOP",

            None

        )


    # ====================================
    # UNKNOWN COMMAND
    # ====================================

    return (

        "UNKNOWN",

        text

    )

