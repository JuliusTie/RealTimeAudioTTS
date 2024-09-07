# Audio Text-to-Speech Application

This Python script provides an automated solution to convert text input into speech using the ElevenLabs API and plays it through the VB-CABLE audio driver. The script continuously monitors the folder for new audio files and plays the most recently generated file.

## Features
- **Text-to-Speech Conversion**: Converts input text to speech using the ElevenLabs API and saves the resulting audio as an MP3 file.
- **VB-CABLE Audio Playback**: Plays the generated audio through the VB-CABLE virtual audio driver.
- **Automatic Audio Monitoring**: Continuously monitors the `audio_files` folder for new audio files and plays the latest one automatically.

## Dependencies
- `pyaudio`: Used to handle audio playback.
- `pydub`: Library for manipulating and playing audio files.
- `requests`: Used to send API requests to ElevenLabs for text-to-speech conversion.
- `threading`: Manages background monitoring of the folder for new audio files.

### Installation

1. Install the required libraries using `pip`:

```bash
pip install pyaudio pydub requests
