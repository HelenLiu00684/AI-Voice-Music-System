
# semantic_ai.py

import os
from openai import OpenAI


# ============================================
# AI SEMANTIC LAYER
# ============================================
#
# Responsibility:
#
#     Convert natural language music
#     requests into structured semantic
#     entities using OpenAI.
#
# This module DOES:
#
#     - interpret ambiguous requests
#     - extract music-related entities
#     - generate structured metadata
#
# This module DOES NOT:
#
#     - search YouTube
#     - download music
#     - play audio
#     - manage playlists
#
# Design Flow:
#
#        User Request
#              ↓
#         OpenAI Model
#              ↓
#      Semantic Entities
#              ↓
#        Query Builder
#              ↓
#       YouTube Search
#
# Design Principle:
#
#     Separate semantic understanding
#     from downstream retrieval logic.
#
# Current Status:
#
#     This module is optional in the
#     current command-based workflow.
#
#     It is preserved as the foundation
#     for future semantic search upgrades.
#
# ============================================


# ============================================
# OPENAI CLIENT
# ============================================
#
# API keys should be stored using
# environment variables.
#
# Example:
#
#     Windows:
#
#         OPENAI_API_KEY
#
# Never hardcode API keys directly
# into source code repositories.
#
# ============================================

client = OpenAI(

    api_key=os.getenv(

        "OPENAI_API_KEY"

    )

)


# ============================================
# AI SEMANTIC ANALYSIS
# ============================================

def analyze_text(text):

    """
    Analyze natural language music requests
    using OpenAI.

    Input:

        text:
            Raw user speech or text.

    Returns:

        JSON-formatted semantic entities.

    Example:

        Input:

            "the Shakira FIFA song"

        Output:

            {
                "artist":"Shakira",
                "song":"Waka Waka",
                "event":"FIFA World Cup",
                "year":2010
            }

    Processing Flow:

            User Input
                 ↓
           Prompt Creation
                 ↓
           OpenAI Model
                 ↓
         Semantic Parsing
                 ↓
            JSON Output

    Design Notes:

        This function performs semantic
        interpretation rather than
        information retrieval.

        The resulting JSON can be
        consumed by downstream query
        optimization modules.

    Future Usage:

        Example:

            search the Shakira FIFA song

                    ↓

              Semantic AI

                    ↓

             Query Builder

                    ↓

            YouTube Search
    """

    # ====================================
    # SEMANTIC EXTRACTION PROMPT
    # ====================================
    #
    # Guide the language model to extract
    # only structured music-related
    # entities.
    #
    # Target entities:
    #
    #     artist
    #     song
    #     movie
    #     event
    #     mood
    #     year
    #
    # The prompt intentionally requests
    # short JSON output to simplify
    # downstream processing.
    #
    # ====================================

    prompt = f"""
    Analyze this music search request.

    User input:
    {text}

    If the request already contains clear
    search keywords, preserve them.

    Extract the following entities if applicable:

    - artist
    - song
    - movie
    - event
    - mood
    - year

    If information cannot be inferred,
    leave the field empty.

    Return short JSON only.
    """

    try:

        # ====================================
        # OPENAI CHAT COMPLETION
        # ====================================
        #
        # Submit the semantic extraction
        # request to OpenAI.
        #
        # The model returns structured
        # music-related entities in JSON
        # format.
        #
        # ====================================

        response = client.chat.completions.create(

            model="gpt-4.1-mini",

            messages=[

                {

                    "role": "user",

                    "content": prompt

                }

            ]

        )

        content = response.choices[0].message.content

        # ====================================
        # DEBUG OUTPUT
        # ====================================
        #
        # Display raw semantic output from
        # OpenAI for prompt verification
        # and development testing.
        #
        # ====================================

        print("\n====================")
        print("RAW AI RESPONSE")
        print("====================\n")

        print(content)

        print("\n====================\n")

        return content

    except Exception as e:

        # ====================================
        # FAIL GRACEFULLY
        # ====================================
        #
        # Return an empty semantic result
        # when AI parsing fails.
        #
        # This prevents semantic failures
        # from crashing the overall system.
        #
        # ====================================

        print(

            "AI semantic parsing failed"

        )

        print(e)

        return ""

