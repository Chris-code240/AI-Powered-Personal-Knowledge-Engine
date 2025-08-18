from moviepy import VideoFileClip
import os
import speech_recognition as sr
import random
import string

r = sr.Recognizer()
BASE_TEMP_DIR = "audio_temp_files"
def generate_random_string(length=12):
    """Generates a random string of specified length using letters and digits."""
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for i in range(length))
    return random_string


def extract_audio_from_video(file_path:str):
    """
    Extract audio (.wav) from video file
    """
    try:
        video = VideoFileClip(file_path)
        audio_file = video.audio
        path = f"{BASE_TEMP_DIR}/audio_{generate_random_string()}.wav"
        audio_file.write_audiofile(path)
        return path
    except Exception as e:
        return None



def audio_to_text(file_path:str):
    """
    Extract speech (English) from audio.wav file.
    """
    try:
        with sr.AudioFile(file_path) as source:
            data = r.record(source)
        return r.recognize_google(data)
    except Exception as e:
        return None
    

def transcribe_video(file_path:str):

    audio_path = extract_audio_from_video(file_path)
    if audio_path:
        text = audio_to_text(audio_path)
        os.remove(audio_path)
        return text
    raise Exception("Unknown Error Occured. Check your file path")

print(transcribe_video("billy flowers 🤓.publer.com.mp4"))

