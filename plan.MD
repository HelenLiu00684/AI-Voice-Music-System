# Raspberry Pi Compatibility

This project architecture is designed to be portable to Raspberry Pi with minimal code changes.

The current implementation runs on Windows 11 using:

```python
ao="wasapi"
```

For Raspberry Pi / Linux environments, the audio backend can be changed to:

```python
ao="alsa"
```

or:

```python
ao="pulse"
```

The serial port configuration should also be updated from:

```python
COM3
```

to a Linux serial device such as:

```python
/dev/ttyUSB0
```

or:

```python
/dev/ttyACM0
```

## Compatible Components

The following core system components remain compatible with Raspberry Pi:

* OpenAI semantic parsing
* Speech recognition
* Audio playback
* Serial communication
* Arduino LED control
* Event-driven FSM
* Audio energy analysis

## Architecture Design

The current architecture is intentionally designed to support future migration toward Raspberry Pi embedded AI systems.

The system already follows a modular architecture:

* Voice input layer
* AI semantic layer
* Search / ranking layer
* Audio playback layer
* Audio analysis layer
* Serial communication layer
* Arduino hardware control layer

This design allows the project to evolve toward a portable embedded AI music system with minimal structural changes.
