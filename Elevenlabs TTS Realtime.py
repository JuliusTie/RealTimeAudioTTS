import os
import time
import pyaudio
import threading
from pydub import AudioSegment
import requests
from pydub.playback import play

# Path to the folder in which the audio files are saved
AUDIO_FOLDER = "audio_files"
if not os.path.exists(AUDIO_FOLDER):
    os.makedirs(AUDIO_FOLDER)

# Function for converting text to speech using ElevenLabs API
def text_to_speech(text):
    api_key = ''
    voice_id = ''
    url = f'https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream'
    headers = {
        'xi-api-key': api_key,
        'Content-Type': 'application/json'
    }
    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.75,
            "similarity_boost": 0.75
        }
    }
    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        filename = os.path.join(AUDIO_FOLDER, f"audio_{int(time.time())}.mp3")
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Audio stream saved as {filename}.")
    else:
        print(f"Error: {response.status_code} - {response.text}")

# Function for playing audio via VB-CABLE
def play_audio_through_vbcable(file_path):
    # Lade die Audio-Datei
    audio = AudioSegment.from_file(file_path, format="mp3")

    p = pyaudio.PyAudio()

    # Search for the VB-CABLE output device
    vb_cable_index = None
    for i in range(p.get_device_count()):
        dev = p.get_device_info_by_index(i)
        if "CABLE Input" in dev['name']:  # This is the standard name for VB-CABLE
            vb_cable_index = i
            break

    if vb_cable_index is None:
        print("VB-CABLE device not found.")
        return

    # Open an audio stream that plays the audio via VB-CABLE
    stream = p.open(format=p.get_format_from_width(audio.sample_width),
                    channels=audio.channels,
                    rate=audio.frame_rate,
                    output=True,
                    output_device_index=vb_cable_index)  # Use VB-CABLE

    # Play the audio
    data = audio.raw_data
    stream.write(data)
    
    stream.stop_stream()
    stream.close()
    p.terminate()

# Function for playing the latest audio file in the folder
def play_latest_audio():
    latest_file = max([f for f in os.listdir(AUDIO_FOLDER) if f.endswith('.mp3')],
                      key=lambda f: os.path.getmtime(os.path.join(AUDIO_FOLDER, f)))
    file_path = os.path.join(AUDIO_FOLDER, latest_file)
    play_audio_through_vbcable(file_path)

# Monitoring the folder for new files
def start_audio_monitor():
    last_modified = None
    while True:
        if not os.listdir(AUDIO_FOLDER):
            continue

        latest_file = max([f for f in os.listdir(AUDIO_FOLDER) if f.endswith('.mp3')],
                          key=lambda f: os.path.getmtime(os.path.join(AUDIO_FOLDER, f)))
        latest_file_path = os.path.join(AUDIO_FOLDER, latest_file)
        modified_time = os.path.getmtime(latest_file_path)

        if last_modified is None or modified_time > last_modified:
            last_modified = modified_time
            play_latest_audio()

        time.sleep(1)

# Main programme
if __name__ == "__main__":
    # Start the monitoring thread
    monitor_thread = threading.Thread(target=start_audio_monitor)
    monitor_thread.daemon = True
    monitor_thread.start()

    # Continuous prompt for text
    while True:
        text = input("Enter text: ")
        text_to_speech(text)
