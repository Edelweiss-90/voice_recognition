from django.http import JsonResponse


class NotFoundException(Exception):
    def __init__(self, message='Not found!'):
        self.message = message
        self.status = 404
        super().__init__(self.message)


class AlreadyExistException(Exception):
    def __init__(self, message='Already exist!'):
        self.message = message
        self.status = 409
        super().__init__(self.message)


class InvalidDataException(Exception):
    def __init__(self, message="Invalid data!"):
        self.message = message
        self.status = 400
        super().__init__(self.message)


class InvalidIdException(Exception):
    def __init__(self, message="ID must be an integer!"):
        self.message = message
        self.status = 400
        super().__init__(self.message)


class EmptyFileException(Exception):
    def __init__(self, message="Empty file uploaded!"):
        self.message = message
        self.status = 400
        super().__init__(self.message)


class UnsupportedFormatException(Exception):
    def __init__(self, message="File format not supported!"):
        self.message = message
        self.status = 400
        super().__init__(self.message)


class FileSizeExceededException(Exception):
    def __init__(self, max_size):
        self.message = f"File size exceeds {max_size} MB limit"
        self.status = 400
        super().__init__(self.message)


def handle_validation_errors(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (
            NotFoundException,
            InvalidDataException,
            InvalidIdException,
            EmptyFileException,
            UnsupportedFormatException,
            FileSizeExceededException,
            AlreadyExistException
        ) as e:
            return JsonResponse({"error": e.message}, status=e.status)
    return wrapper
