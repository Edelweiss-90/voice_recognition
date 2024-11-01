from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import (
    authenticate,
    login as auth_login,
    logout as auth_logout
)

from tools import BaseViews, user_validator


class UserViews(BaseViews):
    _instance = None
    __model = User

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(UserViews, cls).__new__(cls)
        return cls._instance

    @method_decorator(require_POST)
    @user_validator
    def create(self, request):
        user = self._loads_data(request)

        if UserViews.__model.objects.filter(username=user['username']).exists():
            return self._response_error(
                'User with this name already exists!'
                )

        user = UserViews.__model.objects.create_user(**user)
        return self._response_success(f'user created with id: {user.id}')

    @method_decorator(require_POST)
    @user_validator
    def login(self, request):
        user = self._loads_data(request)
        auth = authenticate(**user)

        if auth is not None:
            auth_login(request, auth)
            return self._response_success('login')

        return self._response_error('user not found')

    @method_decorator(require_POST)
    @method_decorator(login_required)
    def logout(self, request):
        auth_logout(request)
        return self._response_success('logout')
