import shutil
from django.contrib.auth import get_user_model
from models import File, Recognizer
from tools import DeletedStatuses
from django.core.files.uploadedfile import SimpleUploadedFile
import os

from django.conf import settings

CONTENT_TYPE = 'application/json'
UPLOAD_DIR = 'test_store'


def create_test_store():
    path_store = os.path.join(settings.BASE_DIR, UPLOAD_DIR)
    path_tmp = os.path.join(path_store, settings.TMP_WAV)
    os.makedirs(path_store)
    os.makedirs(path_tmp)


def delete_test_store():
    if os.path.exists(UPLOAD_DIR):
        shutil.rmtree(UPLOAD_DIR)


def create_test_user():
    return get_user_model().objects.create_user(
            **{
                'username': 'Tester',
                'password': '123'
            }
    )


def create_file(user, file_size):
    return File.objects.create(
            user=user,
            title='Test File',
            size=file_size,
            path='testfile.mp3',
            extension='mp3',
            deleted=DeletedStatuses.NOT_DELETED.name
        )


def create_recognizer(user, file):
    return Recognizer.objects.create(
            user=user,
            file=file,
            text='Sample recognized text',
            deleted=DeletedStatuses.NOT_DELETED.name
        )


def create_dummy_file(content):
    return SimpleUploadedFile(
            'testfile.mp3',
            content,
            content_type='audio/mp3'
        )
