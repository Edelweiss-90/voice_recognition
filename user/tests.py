from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
import json


class UserViewsTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.content_type = 'application/json'

        cls.create_url = reverse('create')
        cls.login_url = reverse('login')
        cls.logout_url = reverse('logout')

        cls.user_data = {
            'username': 'Tester',
            'password': '123'
        }

        cls.existing_user_data = {
            'username': 'test',
            'password': 'pad123'
        }

        cls.invalid_user_data = {
            'long_login': {'username': 'tester_name_user_long', 'password': '123'},
            'long_pass': {'username': 'tester', 'password': 'tester_name_user_long'},
            'empty_login': {'username': '', 'password': '123'},
            'empty_pass': {'username': 'tester', 'password': ''},
            'wrong_type_login': {'username': 1, 'password': '123'},
            'wrong_type_pass': {'username': 'tester', 'password': 1}
        }

        cls.user = get_user_model().objects.create_user(
            **cls.existing_user_data
        )

    def post_request(self, url, data):
        return self.client.post(
            url,
            data=json.dumps(data),
            content_type=self.content_type
        )

    def test_create_user(self):
        response = self.post_request(self.create_url, self.user_data)
        self.assertEqual(response.status_code, 200)

    def test_create_user_already_exist(self):
        response = self.post_request(self.create_url, self.existing_user_data)
        self.assertEqual(response.status_code, 409)

    def test_create_user_invalid_data(self):
        for key, data in self.invalid_user_data.items():
            response = self.post_request(self.create_url, data)
            self.assertEqual(response.status_code, 400)

    def test_user_login(self):
        response = self.post_request(self.login_url, self.existing_user_data)
        self.assertEqual(response.status_code, 200)

    def test_user_login_not_found(self):
        response = self.post_request(self.login_url, self.user_data)
        self.assertEqual(response.status_code, 404)

    def test_user_logout(self):
        self.post_request(self.login_url, self.existing_user_data)
        response = self.post_request(self.logout_url, self.existing_user_data)
        self.assertEqual(response.status_code, 200)

    def test_user_logout_not_found(self):
        response = self.post_request(self.logout_url, self.user_data)
        self.assertEqual(response.status_code, 302)
