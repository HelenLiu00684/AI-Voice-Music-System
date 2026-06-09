# AI Voice Music System

## Project Overview

AI Voice Music System is an event-driven music platform that combines Artificial Intelligence, audio processing, and embedded systems.

The project integrates:

* Voice-controlled music interaction
* OpenAI semantic understanding
* YouTube music retrieval
* Real-time audio playback
* Audio energy analysis
* Arduino hardware communication
* Reactive LED visualization

The goal is to demonstrate how AI software systems can interact with embedded hardware through a modular architecture.

---

# System Architecture

```text
User
 ↓
voice.py
 ↓
command_parser.py
 ↓
main.py (Event-Driven FSM)
 ↓
Semantic AI Layer
 ↓
Query Builder
 ↓
YouTube Retrieval
 ↓
Audio Download
 ↓
Playback Engine
 ↓
Audio Energy Analysis
 ↓
LED Engine
 ↓
Arduino Serial Communication
 ↓
2×74HC595 Shift Registers
 ↓
LED Visualization
```

---

# Current Features

## AI Semantic Music Search

The system converts natural language music requests into optimized search queries.

Examples:

```text
search Taylor Swift

↓

Taylor Swift
```

```text
search FIFA 2026

↓

FIFA World Cup 2026
```

```text
search the Shakira FIFA song

↓

Shakira Waka Waka FIFA World Cup 2010
```

Semantic parsing improves search quality while preserving explicit keywords.

---

## Voice-Controlled Commands

Supported commands include:

* Search music
* Save songs
* Play playlists
* Skip songs
* Delete songs
* Clear playlists
* Stop playback

---

## Audio Playback

Features:

* YouTube audio extraction
* Audio-only playback
* Temporary local buffering
* MPV playback backend
* Blocking playback workflow

---

## Audio Energy Analysis

The system extracts simplified energy features from music.

Current implementation includes:

* Chunk-based analysis
* Mono conversion
* Energy normalization
* Threshold-based classification
* Beat-like pulse visualization

Note:

This implementation estimates average signal energy rather than performing true DSP beat detection.

---

## Reactive LED Visualization

The embedded layer supports:

* Arduino serial communication
* Dual 74HC595 shift registers
* Multi-color LED visualization
* Real-time reactive lighting

Current LED Mapping:

| Energy Level | LED Color |
| ------------ | --------- |
| Low          | Blue      |
| Medium       | Green     |
| High         | Yellow    |
| Peak / Pulse | Red       |

---

# Quick Start

## Clone Repository

```bash
git clone <repository-url>

cd AI_music
```

---

## Create Virtual Environment

```bash
python -m venv venv
```

---

## Activate Environment

Windows PowerShell:

```powershell
venv\Scripts\activate
```

Linux / Raspberry Pi:

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run the Project

```bash
python main.py
```

---

# Python Packages and Purpose

| Package           | Installation                  | Purpose               | Used By        |
| ----------------- | ----------------------------- | --------------------- | -------------- |
| openai            | pip install openai            | Semantic AI           | semantic_ai.py |
| SpeechRecognition | pip install SpeechRecognition | Voice recognition     | voice.py       |
| pyaudio           | pip install pyaudio           | Microphone capture    | voice.py       |
| yt-dlp            | pip install yt-dlp            | YouTube retrieval     | main.py        |
| python-mpv        | pip install python-mpv        | Audio playback        | music.py       |
| pyserial          | pip install pyserial          | Arduino communication | main.py        |
| pydub             | pip install pydub             | Audio decoding        | rhythm.py      |
| numpy             | pip install numpy             | Energy analysis       | rhythm.py      |

---

# External Software Requirements

## FFmpeg

Purpose:

Audio decoding and processing.

Verify installation:

```bash
ffmpeg -version
```

---

## MPV Player

Purpose:

Audio playback engine.

Required files:

```text
mpv.exe
libmpv-2.dll
```

---

## Arduino IDE

Purpose:

Upload firmware to Arduino.

# OpenAI API Configuration

Windows PowerShell:

```powershell
setx OPENAI_API_KEY "your_api_key"
```

Restart PowerShell after configuration.

Linux / Raspberry Pi:

```bash
export OPENAI_API_KEY="your_api_key"
```

---

# Security Notice

Do NOT upload API keys to GitHub.

Correct approach:

```python
import os

api_key = os.getenv("OPENAI_API_KEY")
```

Incorrect approach:

```python
api_key = "sk-xxxxxxxxxxxxxxxx"
```

The repository should never contain:

* API keys
* Passwords
* Tokens
* Credentials

Always use environment variables.

---

# Voice Commands

## Supported Commands

| Command     | Example             | Action              |
| ----------- | ------------------- | ------------------- |
| SEARCH      | search Taylor Swift | AI semantic search  |
| SAVE        | save                | Save current song   |
| NEXT        | next                | Play next song      |
| PLAYLIST    | play playlist       | Play saved playlist |
| DELETE SONG | delete song         | Delete current song |
| DELETE LIST | delete playlist     | Clear playlist      |
| STOP        | stop music          | Stop playback       |

---

## Optional Shortcuts

For improved speech recognition accuracy, numerical shortcuts are also supported.

| Shortcut | Equivalent  |
| -------- | ----------- |
| one      | SEARCH      |
| two      | SAVE        |
| three    | NEXT        |
| four     | PLAYLIST    |
| five     | DELETE SONG |
| six      | DELETE LIST |
| seven    | STOP        |

---

# Example Voice Workflow

Search music:

```text
search Taylor Swift
```

Save current song:

```text
save
```

Skip to next song:

```text
next
```

Play saved playlist:

```text
play playlist
```

Delete current song:

```text
delete song
```

Stop playback:

```text
stop music
```

---

# Hardware Requirements

The current implementation uses:

* Arduino Mega 2560
* Two 74HC595 shift registers
* 16 LEDs
* 220Ω–330Ω resistors
* Breadboard
* Jumper wires
* USB serial connection

---

# Project Structure

```text
AI_music/
│
├── main.py
├── state.py
├── voice.py
├── command_parser.py
├── semantic_ai.py
├── query_builder.py
├── ai_query.py
├── music.py
├── rhythm.py
├── led_engine.py
├── playlist.py
│
├── arduino_mul_led/
│   ├── arduino_led_muti.ino
│   ├── connection.txt
│   ├── test_serial.py
│   └── test_all_led.py
│
├── temp/
├── requirements.txt
└── README.md
```

---

# Runtime State Design

The application maintains a centralized runtime state.

```text
Voice Commands
       ↓
command_parser.py
       ↓
main.py
       ↓
state.py
       ↓
Other Functional Modules
```

This design allows different modules to coordinate playback, playlist management, LED behavior, and microphone control through a shared state model.

---

# Event-Driven Architecture

The system behaves similarly to an event-driven finite state machine.

```text
Events
   ↓
Voice Commands
   ↓
Command Parser
   ↓
State Transition
   ↓
Action Execution
```

Examples of events include:

* SEARCH
* SAVE
* NEXT
* PLAYLIST
* DELETE SONG
* DELETE LIST
* STOP
* Serial Interrupt (MIC)

---

# Serial Interrupt Behavior

Arduino can interrupt the software system through serial communication.

Example:

```text
Arduino
   ↓
MIC
   ↓
Stop Playback
   ↓
Stop LEDs
   ↓
Reopen Microphone
```

This mechanism enables hardware-triggered interaction with the software workflow.

# Hardware Architecture

The LED visualization subsystem uses an Arduino Mega and two cascaded 74HC595 shift registers to drive 16 LEDs while minimizing GPIO usage.

System Flow:

```text
Music Playback
      ↓
Audio Energy Analysis
      ↓
LED Engine
      ↓
Serial Communication
      ↓
Arduino Mega
      ↓
2 × 74HC595
      ↓
16 LEDs
```

---

# 74HC595 Wiring Table

## Arduino Mega → 74HC595 #1

| Arduino Mega | Pin | 74HC595 #1 |   Pin | Purpose |               |
| ------------ | --: | ---------- | ----: | ------- | ------------- |
| Arduino Mega |  D8 | 74HC595 #1 |   SER | 14      | Serial Data   |
| Arduino Mega |  D9 | 74HC595 #1 | SRCLK | 11      | Shift Clock   |
| Arduino Mega | D10 | 74HC595 #1 |  RCLK | 12      | Latch Clock   |
| Arduino Mega |  5V | 74HC595 #1 |   VCC | 16      | Power         |
| Arduino Mega | GND | 74HC595 #1 |   GND | 8       | Ground        |
| Arduino Mega | GND | 74HC595 #1 |    OE | 13      | Enable Output |
| Arduino Mega |  5V | 74HC595 #1 | SRCLR | 10      | Disable Reset |

---

## Cascaded Connection

| Source     |   Pin | Destination |        Pin | Purpose |    |              |
| ---------- | ----: | ----------- | ---------: | ------- | -- | ------------ |
| 74HC595 #1 |   QH' | 9           | 74HC595 #2 | SER     | 14 | Cascade Data |
| 74HC595 #1 | SRCLK | 11          | 74HC595 #2 | SRCLK   | 11 | Shared Clock |
| 74HC595 #1 |  RCLK | 12          | 74HC595 #2 | RCLK    | 12 | Shared Latch |

---

## Power Connections for 74HC595 #2

| Arduino Mega | Pin | 74HC595 #2 |   Pin | Purpose |               |
| ------------ | --: | ---------- | ----: | ------- | ------------- |
| Arduino Mega |  5V | 74HC595 #2 |   VCC | 16      | Power         |
| Arduino Mega | GND | 74HC595 #2 |   GND | 8       | Ground        |
| Arduino Mega | GND | 74HC595 #2 |    OE | 13      | Enable Output |
| Arduino Mega |  5V | 74HC595 #2 | SRCLR | 10      | Disable Reset |

---

# LED Mapping Table

## 74HC595 #1

| Output  | LED Function |
| ------- | ------------ |
| QA (15) | RED1         |
| QB (1)  | RED2         |
| QC (2)  | RED3         |
| QD (3)  | RED4         |
| QE (4)  | YELLOW1      |
| QF (5)  | YELLOW2      |
| QG (6)  | YELLOW3      |
| QH (7)  | YELLOW4      |

---

## 74HC595 #2

| Output  | LED Function |
| ------- | ------------ |
| QA (15) | GREEN1       |
| QB (1)  | GREEN2       |
| QC (2)  | GREEN3       |
| QD (3)  | GREEN4       |
| QE (4)  | BLUE1        |
| QF (5)  | BLUE2        |
| QG (6)  | BLUE3        |
| QH (7)  | BLUE4        |

---

# LED Wiring Rule

Each LED should be connected using a current-limiting resistor.

```text
74HC595 Output
        ↓
220Ω–330Ω Resistor
        ↓
LED Anode (+)
        ↓
LED Cathode (-)
        ↓
GND
```

---

# LED Layout

The current implementation uses four groups of LEDs:

```text
RED:
R1  R2  R3  R4

YELLOW:
Y1  Y2  Y3  Y4

GREEN:
G1  G2  G3  G4

BLUE:
B1  B2  B3  B4
```

---

# Raspberry Pi Compatibility

The software architecture is designed for future Raspberry Pi deployment.

## Audio Backend

Windows:

```text
ao="wasapi"
```

Linux / Raspberry Pi:

```text
ao="alsa"

or

ao="pulse"
```

---

## Serial Port

Windows:

```text
COM3
```

Linux / Raspberry Pi:

```text
/dev/ttyUSB0

or

/dev/ttyACM0
```

---

## Portable Modules

The following modules require little or no modification during migration:

* voice.py
* semantic_ai.py
* query_builder.py
* ai_query.py
* music.py
* rhythm.py
* led_engine.py
* playlist.py
* state.py

---

# Future Development

## AI Semantic Search

Potential improvements include:

* Improved prompt engineering
* Better search ranking
* Richer semantic understanding
* Context-aware recommendations

---

## Advanced Audio Analysis

Possible future enhancements:

* Beat detection
* BPM estimation
* Onset detection
* Frequency band analysis
* Music visualization effects

---

## LED Improvements

Potential upgrades:

* PWM brightness control
* Dynamic animations
* RGB LED support
* Addressable LED strips
* More than 16 channels

---

## Raspberry Pi Deployment

Long-term goals include:

* Standalone embedded deployment
* Local audio playback
* Portable hardware packaging
* Reduced dependency on desktop systems

---

# Educational Purpose

This project was developed as an educational demonstration combining multiple disciplines:

* Artificial Intelligence
* Embedded Systems
* Audio Processing
* Event-Driven Programming
* Serial Communication
* Human-Computer Interaction
* Reactive Visualization

The project demonstrates how AI software can interact with physical hardware through a modular software architecture.

---

# Design Philosophy

The system emphasizes the following principles:

```text
Separation of Concerns
        ↓
Modular Components
        ↓
Event-Driven Coordination
        ↓
Hardware Abstraction
        ↓
Portable Architecture
```

Each module has a clearly defined responsibility, making the system easier to understand, maintain, test, and extend.

---

# Acknowledgements

This project was developed as part of an academic group project exploring the integration of AI technologies with embedded hardware systems.

Special thanks to instructors, teammates, and open-source communities whose tools and documentation made this work possible.
