# semantic_ai.py

import os
from openai import OpenAI


# ============================================
# OPENAI CLIENT
# ============================================
#
# API key should be stored in:
#
# Windows:
#     OPENAI_API_KEY environment variable
#
# Never hardcode API keys directly
# into source code.
#
# ============================================

client = OpenAI(

    api_key=os.getenv("OPENAI_API_KEY")
)


# ============================================
# AI SEMANTIC ANALYSIS
# ============================================
#
# This module converts raw user speech
# into structured semantic music metadata.
#
# Example:
#
# Input:
#     "Shakira FIFA 2010"
#
# Output:
# {
#   "artist": "Shakira",
#   "song": "Waka Waka",
#   "event": "FIFA World Cup",
#   "year": 2010
# }
#
# The purpose of this layer is:
#
# raw speech
#     →
# semantic understanding
#     →
# structured search entities
#
# ============================================

def analyze_text(text):

    """
    Analyze user speech using OpenAI.

    Returns:
        JSON-formatted semantic result.
    """

    # ====================================
    # AI PROMPT
    # ====================================

    prompt = f"""
    Analyze this music request.

    User input:
    {text}

    Return:
    - artist
    - song
    - movie
    - event
    - mood
    - year

    Return short JSON only.
    """

    try:

        # ====================================
        # OPENAI CHAT COMPLETION
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

        print("\n====================")
        print("RAW AI RESPONSE")
        print("====================\n")

        print(content)

        print("\n====================\n")

        return content

    except Exception as e:

        print("AI semantic parsing failed")

        print(e)

        return ""