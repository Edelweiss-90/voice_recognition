import json
import os
import shutil
from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from tools import MemorySizes
from test_tools import (
    create_test_user,
    create_file,
    create_dummy_file,
    create_test_store,
    delete_test_store,
    CONTENT_TYPE,
    UPLOAD_DIR,
)


class UploaderTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        create_test_store()
        
        settings.UPLOAD_DIR = UPLOAD_DIR

        cls.user = create_test_user()
        cls.byte = bytes([0x49])

        cls.dummy_file = create_dummy_file(cls.byte)

        cls.file_instance = create_file(cls.user, cls.dummy_file.size)

        cls.delete_url = reverse('uploader:delete')
        cls.list_url = reverse('uploader:list')
        cls.upload_url = reverse('uploader:upload')

    @classmethod
    def tearDownClass(cls):
        delete_test_store()
        super().tearDownClass()

    def post_request_upload(self, url, data):
        return self.client.post(
            url,
            data=data,
            format='multipart'
        )

    def post_request(self, url, data):
        return self.client.post(
            url,
            data=json.dumps(data),
            content_type=CONTENT_TYPE
        )

    def get_request(self, url, params=None):
        return self.client.get(
            url,
            data=params,
        )

    def test_upload(self):
        self.client.force_login(self.user)

        audio = {
            'file': self.dummy_file
        }

        response = self.post_request_upload(self.upload_url, audio)
        self.assertEqual(response.status_code, 200)

    def test_upload_invalid_extension(self):
        self.client.force_login(self.user)

        audio = {
            'file': SimpleUploadedFile('test.mp4', self.byte)
        }

        response = self.post_request_upload(self.upload_url, audio)
        self.assertEqual(response.status_code, 400)

    def test_upload_exceeds_max_size(self):
        self.client.force_login(self.user)
        file_size = MemorySizes.ONE_MB.value * (
            settings.MAX_FILE_SIZE_IN_MB + 1
        )
        large_file_content = self.byte * file_size

        audio = {
            'file': SimpleUploadedFile('test.mp3', large_file_content)
        }

        response = self.post_request_upload(self.upload_url, audio)
        self.assertEqual(response.status_code, 400)

    def test_upload_empty(self):
        self.client.force_login(self.user)

        response = self.post_request_upload(self.upload_url, {})
        self.assertEqual(response.status_code, 400)

    def test_upload_auth(self):
        response = self.post_request_upload(self.upload_url, {})
        self.assertEqual(response.status_code, 302)

    def test_get_list_auth(self):
        response = self.get_request(self.list_url)
        self.assertEqual(response.status_code, 302)

    def test_file_by_id(self):
        self.client.force_login(self.user)
        url = reverse('uploader:file_by_id', kwargs={
            'id': self.file_instance.id
        })
        response = self.get_request(url)
        self.assertEqual(response.status_code, 200)

    def test_file_by_id_not_found(self):
        self.client.force_login(self.user)
        url = reverse('uploader:file_by_id', kwargs={'id': 10000})
        response = self.get_request(url)
        self.assertEqual(response.status_code, 404)

    def test_file_by_id_auth(self):
        url = reverse('uploader:file_by_id', kwargs={
            'id': self.file_instance.id
        })
        response = self.get_request(url)
        self.assertEqual(response.status_code, 302)

    def test_delete(self):
        self.client.force_login(self.user)
        response = self.post_request(self.delete_url, {
            'id': self.file_instance.id
        })
        self.assertEqual(response.status_code, 200)

    def test_delete_invalid_type(self):
        self.client.force_login(self.user)
        response = self.post_request(self.delete_url, {'id': []})
        self.assertEqual(response.status_code, 400)

    def test_delete_auth(self):
        response = self.post_request(self.delete_url, {'id': []})
        self.assertEqual(response.status_code, 302)
