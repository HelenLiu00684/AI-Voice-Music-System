
# voice.py

import speech_recognition as sr


def listen():

    recognizer = sr.Recognizer()

    with sr.Microphone() as source:

        print(
            "Speak now..."
        )

        recognizer.adjust_for_ambient_noise(

            source,

            duration=0.5

        )

        audio = recognizer.listen(

            source,

            timeout=None,

            phrase_time_limit=10

        )

    try:

        text = recognizer.recognize_google(

            audio

        )

        return text


    except sr.UnknownValueError:

        print(

            "\nDidn't catch that."

        )

        return ""


    except sr.RequestError:

        print(

            "\nSpeech service unavailable."

        )

        return ""


    except Exception as e:

        print(

            "\nVoice error"

        )

        print(e)

        return ""

