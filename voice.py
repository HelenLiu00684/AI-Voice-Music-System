
# voice.py

import speech_recognition as sr


# ============================================
# VOICE INPUT LAYER
# ============================================
#
# Responsibility:
#
#     Capture user speech through the
#     system microphone and convert it
#     into text commands.
#
# This module DOES:
#
#     - open the microphone
#     - calibrate ambient noise
#     - record speech input
#     - invoke speech recognition
#     - return recognized text
#
# This module DOES NOT:
#
#     - parse commands
#     - search music
#     - control playback
#     - manage playlists
#     - drive LED visualization
#
# Design Flow:
#
#        User Speech
#             ↓
#        Microphone
#             ↓
#       Audio Capture
#             ↓
#      Speech Recognition
#             ↓
#        Recognized Text
#             ↓
#      Command Parser
#
# Design Principle:
#
#     Separate speech acquisition from
#     downstream command processing.
#
# ============================================


# ============================================
# MICROPHONE LISTENING
# ============================================

def listen():

    """
    Capture speech from the microphone
    and convert it into text.

    Returns:

        text:
            Recognized speech string.

        "":
            Empty string when recognition
            fails.

    Processing Flow:

            Microphone
                 ↓
         Noise Calibration
                 ↓
           Audio Capture
                 ↓
        Google Recognition
                 ↓
          Recognized Text

    Design Notes:

        The function fails gracefully by
        returning an empty string instead
        of raising exceptions.

        This prevents voice recognition
        failures from terminating the
        entire application.
    """

    # ====================================
    # CREATE SPEECH RECOGNIZER
    # ====================================
    #
    # Instantiate a recognizer used for
    # speech processing.
    #
    # ====================================

    recognizer = sr.Recognizer()

    # ====================================
    # OPEN MICROPHONE
    # ====================================
    #
    # Access the default system
    # microphone as the audio source.
    #
    # ====================================

    with sr.Microphone() as source:

        print(

            "Speak now..."

        )

        # ====================================
        # AMBIENT NOISE CALIBRATION
        # ====================================
        #
        # Adjust the energy threshold to
        # compensate for background noise.
        #
        # This improves recognition
        # robustness in noisy environments.
        #
        # ====================================

        recognizer.adjust_for_ambient_noise(

            source,

            duration=0.5

        )

        # ====================================
        # AUDIO CAPTURE
        # ====================================
        #
        # Record user speech.
        #
        # timeout:
        #     None
        #
        #     Wait indefinitely until the
        #     user begins speaking.
        #
        # phrase_time_limit:
        #     10 seconds
        #
        #     Limit the maximum speech
        #     duration for a single command.
        #
        # ====================================

        audio = recognizer.listen(

            source,

            timeout=None,

            phrase_time_limit=10

        )

    try:

        # ====================================
        # GOOGLE SPEECH RECOGNITION
        # ====================================
        #
        # Convert recorded audio into text
        # using Google's recognition
        # service.
        #
        # ====================================

        text = recognizer.recognize_google(

            audio

        )

        return text

    except sr.UnknownValueError:

        # ====================================
        # UNRECOGNIZED SPEECH
        # ====================================
        #
        # Audio was captured successfully,
        # but the spoken words could not
        # be interpreted.
        #
        # ====================================

        print(

            "\nDidn't catch that."

        )

        return ""

    except sr.RequestError:

        # ====================================
        # SERVICE UNAVAILABLE
        # ====================================
        #
        # The recognition service could
        # not be reached.
        #
        # Possible causes:
        #
        #     - no internet connection
        #     - Google service unavailable
        #
        # ====================================

        print(

            "\nSpeech service unavailable."

        )

        return ""

    except Exception as e:

        # ====================================
        # UNEXPECTED ERROR
        # ====================================
        #
        # Handle unforeseen failures
        # gracefully without crashing
        # the application.
        #
        # ====================================

        print(

            "\nVoice error"

        )

        print(e)

        return ""

