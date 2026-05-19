import speech_recognition as sr


def listen():

    r = sr.Recognizer()

    with sr.Microphone() as source:

        print("Speak now...")

        audio = r.listen(source)

    try:

        text = r.recognize_google(audio)

        return text

    except Exception as e:

        print("Speech recognition failed")

        print(e)

        return ""
