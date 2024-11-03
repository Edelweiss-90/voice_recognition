from io import BytesIO
from django.test import TestCase
from django.urls import reverse
import json
from pydub.generators import Sine
from django.conf import settings

from test_tools import (
    create_test_user,
    create_file,
    create_recognizer,
    create_dummy_file,
    create_test_store,
    delete_test_store,
    UPLOAD_DIR,
    CONTENT_TYPE
)


class RecognizerTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        create_test_store()

        settings.UPLOAD_DIR = UPLOAD_DIR

        cls.user = create_test_user()

        sine_wave = Sine(440).to_audio_segment(duration=1000)
        mp3_data = BytesIO()
        sine_wave.export(mp3_data, format="mp3")

        cls.dummy_file = create_dummy_file(
            mp3_data.getvalue()
        )

        cls.file_instance = create_file(cls.user, cls.dummy_file.size)

        cls.recognizer_instance = create_recognizer(
            cls.user, cls.file_instance
        )

        cls.delete_url = reverse('recognizer:delete')
        cls.recognize_url = reverse('recognizer:recognize')

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = cls.client_class()
        cls.client.force_login(cls.user)
        response = cls.client.post(reverse('uploader:upload'), {
            'file': cls.dummy_file
        })
        cls.file_id = response.json()['success']

        assert response.status_code == 200

    @classmethod
    def tearDownClass(cls):
        delete_test_store()
        super().tearDownClass()

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

    def test_recognize(self):
        self.client.force_login(self.user)

        response = self.post_request(self.recognize_url, {
            'file_id': self.file_id,
            'language': 'ru-RU'
        })
        self.assertEqual(response.status_code, 200)

    def test_recognize_empty_params(self):
        self.client.force_login(self.user)

        response = self.post_request(self.recognize_url, {})
        self.assertEqual(response.status_code, 400)

    def test_recognize_not_found(self):
        self.client.force_login(self.user)

        response = self.post_request(self.recognize_url, {
            'file_id': 1000,
            'language': 'ru-RU'
        })
        self.assertEqual(response.status_code, 404)

    def test_recognize_not_support_language(self):
        self.client.force_login(self.user)

        response = self.post_request(self.recognize_url, {
            'file_id': 1000,
            'language': 'ar'
        })
        self.assertEqual(response.status_code, 400)

    def test_recognize_auth(self):
        response = self.post_request(self.recognize_url, {})
        self.assertEqual(response.status_code, 302)

    def test_recognize_id(self):
        self.client.force_login(self.user)
        url = reverse('recognizer:recognize_id', kwargs={
            'id': self.recognizer_instance.id
        })
        response = self.get_request(url)
        self.assertEqual(response.status_code, 200)

    def test_recognize_id_not_found(self):
        self.client.force_login(self.user)
        url = reverse('recognizer:recognize_id', kwargs={'id': 10000})
        response = self.get_request(url)
        self.assertEqual(response.status_code, 404)

    def test_recognize_id_auth(self):
        url = reverse('recognizer:recognize_id', kwargs={
            'id': self.recognizer_instance.id
        })
        response = self.get_request(url)
        self.assertEqual(response.status_code, 302)
    
    def test_list_by_file_id(self):
        self.client.force_login(self.user)
        url = reverse('recognizer:list_by_file_id', kwargs={
            'id': self.file_instance.id
        })
        response = self.get_request(url)
        self.assertEqual(response.status_code, 200)

    def test_list_by_file_id_not_found(self):
        self.client.force_login(self.user)
        url = reverse('recognizer:list_by_file_id', kwargs={'id': 10000})
        response = self.get_request(url)
        self.assertEqual(response.status_code, 404)

    def test_list_by_file_id_auth(self):
        url = reverse('recognizer:list_by_file_id', kwargs={
            'id': self.file_instance.id
        })
        response = self.get_request(url)
        self.assertEqual(response.status_code, 302)

    def test_delete(self):
        self.client.force_login(self.user)
        response = self.post_request(self.delete_url, {
            'id': self.recognizer_instance.id
        })
        self.assertEqual(response.status_code, 200)

    def test_delete_invalid_type(self):
        self.client.force_login(self.user)
        response = self.post_request(self.delete_url, {'id': []})
        self.assertEqual(response.status_code, 400)

    def test_delete_auth(self):
        response = self.post_request(self.delete_url, {'id': []})
        self.assertEqual(response.status_code, 302)
