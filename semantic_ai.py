# semantic_ai.py

from openai import OpenAI
import os
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def analyze_text(text):

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

    print("\n====================")
    print("RAW AI RESPONSE")
    print("====================\n")

    print(content)

    print("\n====================\n")

    return content

# Content format:
# {
#   "artist": "Shakira",
#   "song": "Waka Waka",
#   "event": "FIFA World Cup",
#   "year": 2010
# }
# 