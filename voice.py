# voice.py

import speech_recognition as sr


# ============================================
# MICROPHONE LISTENING
# ============================================

def listen():

    # Create speech recognizer
    recognizer = sr.Recognizer()

    # Open default system microphone
    with sr.Microphone() as source:

        print("Speak now...")

        # ====================================
        # ADJUST FOR BACKGROUND NOISE
        # ====================================

        recognizer.adjust_for_ambient_noise(
            source,
            duration=0.5
        )

        # ====================================
        # RECORD AUDIO
        # ====================================

        audio = recognizer.listen(

            source,

            timeout=5,

            phrase_time_limit=10
        )

    try:

        # ====================================
        # GOOGLE SPEECH RECOGNITION
        # ====================================

        text = recognizer.recognize_google(audio)

        return text

    except Exception as e:

        print("Speech recognition failed")

        print(e)

        return ""
