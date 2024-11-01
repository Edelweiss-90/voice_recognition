from django.views.decorators.http import require_GET
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from models import Recognizer, File
from tools import BaseViews, text_audio, id_validator


class RecognizerViews(BaseViews):
    _instance = None
    __file = File
    __model = Recognizer

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RecognizerViews, cls).__new__(cls)
        return cls._instance

    @method_decorator(require_GET)
    @method_decorator(login_required)
    @id_validator
    def recognize(self, request, id):
        file = self.__file.objects.filter(
            id=id, user_id=request.user.id
        ).exists()

        if not file:
            return self._response_error('Not found!')

        file = self.__file.objects.get(id=id)
        text = text_audio(file.path)

        data = self.__model.objects.create(
            text=text,
            user_id=request.user.id,
            file_id=id,
        )

        return self._response_success(data.id)

    @method_decorator(require_GET)
    @method_decorator(login_required)
    @id_validator
    def get_by_id(self, request, id):
        record = self.__model.objects.filter(
            id=id, user_id=request.user.id
        ).exists()

        if not record:
            return self._response_error('Not found!')

        record = self.__model.objects.get(
            id=id, user_id=request.user.id
        )

        return self._response_success({
            'id': record.id,
            'text': record.text
        })
