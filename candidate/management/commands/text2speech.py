
# => pip install gtts pydub
# => pip install pyaudio
# => Also system should contain ffmpeg else visit https://github.com/BtbN/FFmpeg-Builds/releases and get for the os and extract in 
#     C:ffmpeg (create the directory). Then its bin path to system environment path 
# => Just get into this file directory in terminal and run py text2speech.py


import os
from gtts import gTTS
from io import BytesIO
from pydub import AudioSegment
from pydub.playback import play
import tempfile
import wave
import pyaudio

def play_audio(file_path):
    # Play the audio using PyAudio
    chunk = 1024
    wf = wave.open(file_path, 'rb')
    p = pyaudio.PyAudio()

    # Open stream
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    # Read data
    data = wf.readframes(chunk)

    # Play stream
    while data:
        stream.write(data)
        data = wf.readframes(chunk)

    # Stop stream
    stream.stop_stream()
    stream.close()

    # Close PyAudio
    p.terminate()

def text_to_speech_malayalam(text):
    # Convert text to speech in Malayalam
    tts = gTTS(text, lang='ml')
    # Save the speech to a BytesIO object
    speech_io = BytesIO()
    tts.write_to_fp(speech_io)
    # Seek to the start of the BytesIO object
    speech_io.seek(0)
    # Load the BytesIO object into an AudioSegment
    audio = AudioSegment.from_file(speech_io, format="mp3")

    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_audio_path = os.path.join(temp_dir, "temp_audio.wav")
        # Export audio to a temporary file
        audio.export(temp_audio_path, format="wav")
        # Play the audio
        play_audio(temp_audio_path)

# Example usage
malayalam_text = "ഐ.എസ്.ആർ.ഓയിൽ  നിന്ന് റാം സിങ് ആവശ്യപ്പെടുന്ന ഗാനം ............................ പുലി ഉറുമുദ്‌ പുലി ഉറുമുദ്‌  ഇടി ഇടിക്കിത് ഇടി ഇടിക്കിത് കൊടി പറക്കിത് കൊടി പറക്കിത്  വേട്ടക്കാരവരാതപാത്ത്"
text_to_speech_malayalam(malayalam_text)
