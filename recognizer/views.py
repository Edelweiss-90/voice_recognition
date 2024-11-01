from django.views.decorators.http import require_GET, require_POST
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from models import Recognizer, File
from tools import (
    BaseViews,
    text_audio,
    id_validator,
    NotFoundException,
    handle_validation_errors,
    recognize_param_validator
    )


class RecognizerViews(BaseViews):
    _instance = None
    __file = File
    __model = Recognizer

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RecognizerViews, cls).__new__(cls)
        return cls._instance

    @method_decorator(require_POST)
    @method_decorator(login_required)
    @handle_validation_errors
    @recognize_param_validator
    def recognize(self, request):
        file_id = self._loads_data(request)['file_id']
        
        file = self.__file.objects.filter(
            id=file_id, user_id=request.user.id
        ).exists()

        if not file:
            raise NotFoundException()

        file = self.__file.objects.get(id=file_id)
        text = text_audio(file.path)
        print(file_id, text, request.user.id)
        
        data = self.__model.objects.create(
            file_id=file_id,
            text=text,
            user_id=request.user.id,
        )
        print(5)

        return self._response_success({
            'id': data.id,
            'text': text
        })

    @method_decorator(require_GET)
    @method_decorator(login_required)
    @handle_validation_errors
    @id_validator
    def recognize_id(self, request, id):
        record = self.__model.objects.filter(
            id=id, user_id=request.user.id
        ).exists()

        if not record:
            raise NotFoundException()

        record = self.__model.objects.get(
            id=id, user_id=request.user.id
        )

        return self._response_success({
            'id': record.id,
            'text': record.text
        })

    @method_decorator(require_GET)
    @method_decorator(login_required)
    @handle_validation_errors
    @id_validator
    def list_by_file_id(self, request, id):
        file = self.__file.objects.filter(
            id=id, user_id=request.user.id
        ).exists()

        if not file:
            raise NotFoundException()

        records = self.__model.objects.filter(
            file_id=id
        )

        return self._response_success([
                                        {'id': item.id, 'text': item.text}
                                        for item in records
                                    ])
