import os
from django.conf import settings

from .constants import MemorySizes
from .exceptions import (
    InvalidIdException,
    EmptyFileException,
    FileSizeExceededException,
    UnsupportedFormatException,
    InvalidDataException,
    )


def check_req_user_data(data):
    max_length = 12
    min_length = 3
    return type(data) is not str or len(data) > max_length or len(data) < min_length


def user_validator(func):
    def wrapper(self, request):
        valid_data = self._loads_data(request)

        username = valid_data['username']
        password = valid_data['password']

        if check_req_user_data(username):
            raise InvalidDataException()

        if check_req_user_data(password):
            raise InvalidDataException()

        return func(self, request)

    return wrapper


def recognize_param_validator(func):
    def wrapper(self, request):
        valid_data = self._loads_data(request)

        file_id = valid_data['file_id']
        language = valid_data['language']

        if file_id is None or not isinstance(file_id, int):
            raise InvalidIdException()

        if language not in settings.LANGUAGE:
            raise InvalidDataException()

        return func(self, request)

    return wrapper


def id_validator(func):
    def wrapper(self, request, id):
        if id.is_integer():
            return func(self, request, int(id))

        raise InvalidIdException()

    return wrapper


def id_params_validator(func):
    def wrapper(self, request):
        id = self._loads_data(request).get('id')
        if id and type(id) is int:
            return func(self, request)

        raise InvalidIdException()

    return wrapper


def file_validation(func):
    def wrapper(self, request):
        file = request.FILES.get('file')

        if not file:
            raise EmptyFileException()

        file_destination = os.path.splitext(file.name)

        if file_destination[1] not in settings.EXTENSIONS:
            raise UnsupportedFormatException()

        max_size = MemorySizes.ONE_MB.value * settings.MAX_FILE_SIZE_IN_MB
        if file and file.size > max_size:
            raise FileSizeExceededException(max_size)

        return func(self, request)

    return wrapper
