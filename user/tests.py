from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
import json


class UserViewsTests(TestCase):
    def setUp(self):
        self.existing_user_data = {
            'username': 'test',
            'password': 'pad123'
        }

        self.user_data = {
            'username': 'Kirill',
            'password': '123'
        }

        self.user_data_long_login = {
            'username': 'tester_name_user_long',
            'password': '123'
        }

        self.user_data_long_pass = {
            'username': 'tester',
            'password': 'tester_name_user_long'
        }

        self.user_data_empty_login = {
            'username': '',
            'password': '123'
        }

        self.user_data_empty_pass = {
            'username': 'tester',
            'password': ''
        }

        self.user_data_wring_type_login = {
            'username': 1,
            'password': '123'
        }

        self.user_data_wrong_type_pass = {
            'username': 'tester',
            'password': 1
        }

        self.content_type = 'application/json'

        self.create = reverse('create')
        self.login = reverse('login')
        self.logout = reverse('logout')

        self.user = get_user_model().objects.create_user(
            **self.existing_user_data
        )

    def test_create_user(self):
        response = self.client.post(
            self.create,
            data=json.dumps(self.user_data),
            content_type=self.content_type
        )

        self.assertEqual(response.status_code, 200)

    def test_create_user_already_exist(self):
        response = self.client.post(
            self.create,
            data=json.dumps(self.existing_user_data),
            content_type=self.content_type
        )

        self.assertEqual(response.status_code, 409)

    def test_create_user_wrong_data(self):
        response = self.client.post(
            self.create,
            data=json.dumps(self.user_data_long_login),
            content_type=self.content_type
        )

        self.assertEqual(response.status_code, 400)

        response = self.client.post(
            self.create,
            data=json.dumps(self.user_data_long_pass),
            content_type=self.content_type
        )

        self.assertEqual(response.status_code, 400)

    def test_create_user_empty_data(self):
        response = self.client.post(
            self.create,
            data=json.dumps(self.user_data_empty_login),
            content_type=self.content_type
        )

        self.assertEqual(response.status_code, 400)

        response = self.client.post(
            self.create,
            data=json.dumps(self.user_data_empty_pass),
            content_type=self.content_type
        )

        self.assertEqual(response.status_code, 400)

    def test_create_user_wrong_type(self):
        response = self.client.post(
            self.create,
            data=json.dumps(self.user_data_wring_type_login),
            content_type=self.content_type
        )

        self.assertEqual(response.status_code, 400)

        response = self.client.post(
            self.create,
            data=json.dumps(self.user_data_wrong_type_pass),
            content_type=self.content_type
        )

        self.assertEqual(response.status_code, 400)

    def test_user_login(self):
        response = self.client.post(
            self.login,
            data=json.dumps(self.existing_user_data),
            content_type=self.content_type
        )

        self.assertEqual(response.status_code, 200)

    def test_user_login_not_found(self):
        response = self.client.post(
            self.login,
            data=json.dumps(self.user_data),
            content_type=self.content_type
        )

        self.assertEqual(response.status_code, 404)

    def test_user_logout(self):
        self.client.post(
            self.login,
            data=json.dumps(self.existing_user_data),
            content_type=self.content_type
        )

        response = self.client.post(
            self.logout,
            data=json.dumps(self.existing_user_data),
            content_type=self.content_type
        )

        self.assertEqual(response.status_code, 200)

    def test_user_logout_not_found(self):
        response = self.client.post(
            self.logout,
            data=json.dumps(self.user_data),
            content_type=self.content_type
        )

        self.assertEqual(response.status_code, 302)
