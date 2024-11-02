from django.contrib.auth import get_user_model


def create_test_user():
    return get_user_model().objects.create_user(
            **{
                'username': 'Tester',
                'password': '123'
            }
    )
