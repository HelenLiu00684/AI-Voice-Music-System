# AI Voice Music System

An AI-driven reactive music system combining:

- Voice-controlled music search
- OpenAI semantic understanding
- YouTube audio retrieval
- Real-time audio playback
- Audio energy analysis
- Arduino hardware interfacing
- Reactive LED visualization

The system integrates both software and embedded hardware components into a portable event-driven architecture.

---

# Current Features

## AI Semantic Music Search

The system converts natural voice input into semantic music queries.

Example:

```text
"Play the FIFA 2010 song"

↓

Shakira - Waka Waka

The AI layer uses OpenAI semantic parsing to improve music retrieval quality.

Audio Playback
Audio-only playback
YouTube audio extraction
Local audio buffering
Background playback using mpv
Audio Energy Analysis

The system analyzes audio energy in real time and converts music intensity into reactive LED behavior.

Current implementation includes:

chunk-based audio analysis
normalized energy extraction
threshold-based visualization
simple beat-like pulse detection
Arduino Reactive LED System

The hardware layer currently supports:

Arduino serial communication
74HC595 shift register control
Multi-color LED visualization
Real-time reactive lighting

Current LED mapping:

Energy Level	LED Color
Low	Blue
Medium	Green
High	Yellow
Peak / Beat Pulse	Red
System Architecture
Microphone Input
        ↓
Speech Recognition
        ↓
OpenAI Semantic Parsing
        ↓
Search Query Builder
        ↓
YouTube Retrieval
        ↓
Audio Download
        ↓
Audio Playback
        ↓
Audio Energy Analysis
        ↓
LED Reactive Engine
        ↓
Arduino Serial Communication
        ↓
74HC595 + LEDs
Project Structure
AI_music/
│
├── main.py
├── state.py
├── voice.py
├── semantic_ai.py
├── query_builder.py
├── ai_query.py
├── music.py
├── rhythm.py
├── led_engine.py
├── playlist.py
│
├── arduino_led/
│
├── temp/
│
└── README.md
Python Version

Recommended:

Python 3.11
Create Virtual Environment
python -m venv venv
Activate Virtual Environment

Windows PowerShell:

venv\Scripts\activate
Install Required Python Libraries
OpenAI API
pip install openai

Purpose:

AI semantic parsing
Speech Recognition
pip install SpeechRecognition

Purpose:

Microphone speech recognition
PyAudio
pip install pyaudio

Purpose:

Microphone audio capture
yt-dlp
pip install yt-dlp

Purpose:

YouTube music search and audio download
python-mpv
pip install python-mpv

Purpose:

Audio playback backend
pyserial
pip install pyserial

Purpose:

Python ↔ Arduino serial communication
pydub
pip install pydub

Purpose:

Audio energy analysis
numpy
pip install numpy

Purpose:

Audio processing
External Software
FFmpeg

Download:

FFmpeg Official Website

After installation:

ffmpeg -version

It should run correctly from PowerShell.

Purpose:

Audio decoding and processing
mpv Player

Download:

mpv Official Website

Required files:

mpv.exe
libmpv-2.dll

Purpose:

Audio playback engine
Arduino IDE

Download:

Arduino IDE

Purpose:

Upload Arduino firmware
OpenAI API Key

Windows PowerShell:

setx OPENAI_API_KEY "your_api_key"

Restart PowerShell after setting the environment variable.

Important Security Notice

Do NOT upload real API keys to GitHub.

Correct approach:

import os

api_key = os.getenv("OPENAI_API_KEY")

Incorrect approach:

api_key = "sk-xxxxxxxx"
Hardware Requirements

Current hardware setup:

Arduino Uno / Mega
74HC595 shift register
LEDs
Breadboard
Resistors
Push button switch
USB serial connection
Current Reactive LED Logic

The system currently uses:

audio waveform
    →
audio energy extraction
    →
normalized energy values
    →
threshold classification
    →
LED color mapping

This is currently a simplified reactive lighting system rather than true DSP beat detection.

Raspberry Pi Compatibility

This project architecture is designed to be portable to Raspberry Pi with minimal code changes.

The current implementation runs on Windows 11 using:

ao="wasapi"

For Raspberry Pi / Linux environments, the audio backend can be changed to:

ao="alsa"

or:

ao="pulse"

The serial port configuration should also be updated from:

COM3

to a Linux serial device such as:

/dev/ttyUSB0

or:

/dev/ttyACM0
Compatible Components

The following core system components remain compatible with Raspberry Pi:

OpenAI semantic parsing
Speech recognition
Audio playback
Serial communication
Arduino LED control
Event-driven FSM
Audio energy analysis
Current Architecture Design

The current architecture follows a modular event-driven structure:

Voice input layer
AI semantic layer
Retrieval layer
Audio playback layer
Audio analysis layer
Serial communication layer
Hardware control layer

This design allows the project to evolve toward a portable embedded AI music system.

Future Development
1. AI Semantic Query Improvement

Future goals:

improved semantic understanding
better search ranking
improved prompt engineering
richer music context understanding
2. Advanced LED Visualization

Future goals:

improved beat detection
PWM brightness control
advanced rhythm visualization
multi-layer LED effects
dynamic animation modes
3. Raspberry Pi Migration

Future goals:

embedded Linux deployment
portable standalone architecture
optimized hardware integration
portable AI music system
Educational Purpose

This project is currently designed as:

AI + Embedded Systems + Audio Reactive Visualization

It combines:

AI semantic systems
real-time event-driven architecture
serial communication
embedded hardware control
reactive visualization
audio signal quantization