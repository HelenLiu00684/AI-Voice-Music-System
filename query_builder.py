# query_builder.py

import json


def build_query(ai_result):

    # ====================================
    # remove markdown
    # ====================================

    ai_result = ai_result.replace("```json", "")

    ai_result = ai_result.replace("```", "")

    ai_result = ai_result.strip()

    # ====================================
    # json -> dict
    # ====================================

    data = json.loads(ai_result)

    parts = []

    # ====================================
    # IMPORTANT:
    # ONLY KEEP CORE SEARCH ENTITIES
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
    # final query
    # ====================================

    return " ".join(parts)