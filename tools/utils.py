from django.urls import path
from pydub import AudioSegment
import os
import uuid
import speech_recognition as sr
from moviepy.editor import VideoFileClip
from pydub.utils import mediainfo

from django.conf import settings


def create_urls_and_routers(cls, dynamic='/'):
    cls = cls()
    return [
        path(f'{fu_name}{dynamic}', getattr(cls, fu_name))
        for fu_name in dir(cls)
        if callable(getattr(cls, fu_name)) and not fu_name.startswith('_')
    ]


def upload_file(file):
    file_destination = os.path.splitext(file.name)
    file_name = f'{uuid.uuid4()}_{file_destination[0]}'
    with open(
        f'{settings.UPLOAD_DIR}/{file_name}{file_destination[1]}', 'wb+'
    ) as stream:
        for chunk in file.chunks():
            stream.write(chunk)

    return {
        'title': file_name,
        'extension': file_destination[1],
        'size': file.size,
        'path': f'{settings.UPLOAD_DIR}/{file_name + file_destination[1]}'
    }


def get_audio_from_video(video_path):
    video = VideoFileClip(video_path)
    audio_path = "audio.wav"
    video.audio.write_audiofile(audio_path)
    return audio_path


def text_audio(file_path):
    audio_path = f'{settings.BASE_DIR}/{file_path}'
    tmp_audio_name = 'tmp_audio.wav'
    wav_path = f'{settings.BASE_DIR}/{settings.UPLOAD_DIR}/{settings.TMP_WAV}'
    full_path = f'{wav_path}/{tmp_audio_name}'

    AudioSegment.from_file(audio_path).export(full_path, format="wav")

    recognizer = sr.Recognizer()
    audio_file = AudioSegment.from_wav(full_path)
    chunk_length_ms = 30000

    audio_chunks = [audio_file[i:i + chunk_length_ms] for i in range(
        0, len(audio_file), chunk_length_ms
    )]

    full_text = ""

    for i, chunk in enumerate(audio_chunks):
        chunk_wav_path = f"{wav_path.rsplit('.', 1)[0]}_chunk_{i}.wav"
        chunk.export(chunk_wav_path, format="wav")

        with sr.AudioFile(chunk_wav_path) as source:
            print(f"Recognizing chunk {i + 1}/{len(audio_chunks)}...")
            audio = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio, language="ru-RU")
                full_text += text + " "
            except sr.UnknownValueError:
                print(f"Unable to recognize speech in chunk {i + 1}")
            except sr.RequestError as e:
                print(f"Request Error for chunk {i + 1}: {e}")

    for file in os.listdir(wav_path):
        os.unlink(f'{wav_path}/{file}')

    return full_text.strip()
