# query_builder.py

import json


# ============================================
# BUILD SEARCH QUERY
# ============================================
#
# Convert AI semantic JSON output
# into a simplified YouTube search query.
#
# The AI layer extracts semantic meaning,
# while this module focuses only on
# search optimization.
#
# IMPORTANT:
# Mood-related fields are intentionally
# excluded because they reduce
# YouTube search stability.
#
# ============================================

def build_query(ai_result):

    """
    Build a simplified YouTube search query
    from AI semantic parsing results.
    """

    # ====================================
    # REMOVE MARKDOWN WRAPPER
    # ====================================

    ai_result = ai_result.replace(

        "```json",
        ""
    )

    ai_result = ai_result.replace(

        "```",
        ""
    )

    ai_result = ai_result.strip()

    # ====================================
    # JSON STRING → PYTHON DICTIONARY
    # ====================================

    data = json.loads(ai_result)

    parts = []

    # ====================================
    # CORE SEARCH ENTITIES ONLY
    # ====================================
    #
    # Keep only stable search keywords.
    #
    # Avoid:
    # - mood
    # - emotional descriptions
    # - long semantic phrases
    #
    # because they negatively affect
    # YouTube search quality.
    #
    # ====================================

    if data.get("artist"):

        parts.append(str(data["artist"]))

    if data.get("song"):

        parts.append(str(data["song"]))

    if data.get("movie"):

        parts.append(str(data["movie"]))

    if data.get("event"):

        parts.append(str(data["event"]))

    if data.get("year"):

        parts.append(str(data["year"]))

    # ====================================
    # FINAL SEARCH QUERY
    # ====================================

    return " ".join(parts)