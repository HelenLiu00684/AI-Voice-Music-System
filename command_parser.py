
# ============================================
# COMMAND PARSER
# ============================================


def parse_command(text):

    text=text.lower().strip()


    # SEARCH


    if text.startswith(

        ("search ","one ")

    ):

        if text.startswith(

            "search "

        ):

            query=text.replace(

                "search",

                "",

                1

            )

        else:

            query=text.replace(

                "one",

                "",

                1

            )

        query=query.strip()

        return (

            "SEARCH",

            query

        )




    # SAVE

    if text in [

        "save",

        "save into the playlist",

        "write into the playlist",

        "save song",

        "Two",

        "save this song"

    ]:

        return (

            "SAVE",

            None

        )


    # NEXT

    if text in [

        "next",

        "next song",

        "play next song",

        "Three"

    ]:

        return (

            "NEXT",

            None

        )


    # PLAYLIST

    if text in [

        "play list",

        "play playlist",

        "play my playlist",

        "Four"

    ]:

        return (

            "PLAYLIST",

            None

        )


    # DELETE SONG

    if text in [

        "delete song",

        "remove this song",

        "Five"

    ]:

        return (

            "DELETE_SONG",

            None

        )


    # DELETE LIST

    if text in [

        "delete playlist",

        "clear playlist",

        "Six"

    ]:

        return (

            "DELETE_LIST",

            None

        )


    # STOP

    if text in [

        "stop music",

        "stop song",

        "Seven"

    ]:

        return (

            "STOP",

            None

        )


    return (

        "UNKNOWN",

        text

    )
