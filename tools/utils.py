from django.urls import path
from pydub import AudioSegment
import os
import uuid
import speech_recognition as sr
from django.core.files.uploadedfile import UploadedFile
from typing import Type

from django.conf import settings


def create_urls_and_routers(cls: Type):
    cls = cls()
    urls = []
    search_by = '_'

    for method in dir(cls):
        if not method.startswith(search_by) and callable(getattr(cls, method)):
            route = method + '/'
            if search_by in method:
                route = route + f'<int:{method.split('_')[-1]}>'

            urls.append(path(route, getattr(cls, method), name=method))

    return urls


def upload_file(file: UploadedFile):
    file_destination = os.path.splitext(file.name)
    file_name = f'{uuid.uuid4()}_{file_destination[0]}'
    with open(
        f'{settings.UPLOAD_DIR}/{file_name}{file_destination[1]}', 'wb+'
    ) as stream:
        for chunk in file.chunks():
            stream.write(chunk)

    return {
        'title': file_destination[0],
        'extension': file_destination[1],
        'size': file.size,
        'path': f'{settings.UPLOAD_DIR}/{file_name + file_destination[1]}'
    }


def text_audio(file_path: str, language: str):
    audio_path = f'{settings.BASE_DIR}/{file_path}'
    print(audio_path, '<<<<<audio_path path')
    tmp_audio_name = 'tmp_audio.wav'
    wav_path = f'{settings.BASE_DIR}/{settings.UPLOAD_DIR}/{settings.TMP_WAV}'
    print(wav_path, '<<<<<wav_path path')
    full_path = f'{wav_path}/{tmp_audio_name}'
    print(full_path, '<<<<<full_path path')

    print('AudioSegment')
    AudioSegment.from_file(audio_path).export(full_path, format="wav")
    print(1)
    recognizer = sr.Recognizer()
    audio_file = AudioSegment.from_wav(full_path)
    chunk_length_ms = 30000
    print(2)

    audio_chunks = [audio_file[i:i + chunk_length_ms] for i in range(
        0, len(audio_file), chunk_length_ms
    )]
    print(3)

    full_text = ""

    for i, chunk in enumerate(audio_chunks):
        chunk_wav_path = f"{wav_path.rsplit('.', 1)[0]}_chunk_{i}.wav"
        chunk.export(chunk_wav_path, format="wav")

        with sr.AudioFile(chunk_wav_path) as source:
            print(f"Recognizing chunk {i + 1}/{len(audio_chunks)}...")
            audio = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio, language=language)
                full_text += text + " "
            except sr.UnknownValueError:
                print(f"Unable to recognize speech in chunk {i + 1}")
            except sr.RequestError as e:
                print(f"Request Error for chunk {i + 1}: {e}")

    for file in os.listdir(wav_path):
        os.unlink(f'{wav_path}/{file}')

    return full_text.strip()
