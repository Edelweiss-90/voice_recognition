from django.views.decorators.http import require_GET, require_POST
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db import transaction

from models import Recognizer, File
from tools import (
    BaseViews,
    text_audio,
    id_validator,
    id_params_validator,
    NotFoundException,
    handle_validation_errors,
    recognize_param_validator,
    DeletedStatuses,
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
        params = self._loads_data(request)

        file = self.__file.objects.filter(
            id=params['file_id'], user_id=request.user.id
        ).exists()

        if not file:
            raise NotFoundException()

        file = self.__file.objects.get(id=params['file_id'])
        text = text_audio(file.path, params['language'])

        data = self.__model.objects.create(
            file_id=params['file_id'],
            text=text,
            user_id=request.user.id,
        )

        return self._response_success({
            'id': data.id,
            'text': text
        })

    @method_decorator(require_GET)
    @method_decorator(login_required)
    @handle_validation_errors
    @id_validator
    def recognize_id(self, request, id):
        params = {
            'id': id,
            'user_id': request.user.id
        }

        self._check_exist(self.__file, params)

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
        params = {
            'id': id,
            'user_id': request.user.id
        }

        self._check_exist(self.__file, params)

        records = self.__model.objects.filter(
            file_id=id
        )

        return self._response_success([
                                        {'id': item.id, 'text': item.text}
                                        for item in records
                                    ])

    @method_decorator(require_POST)
    @method_decorator(login_required)
    @handle_validation_errors
    @id_params_validator
    @transaction.atomic
    def delete(self, request):
        params = {
            'id': self._loads_data(request)['id'],
            'user_id': request.user.id
        }

        self._check_exist(self.__model, params)

        self.__model.objects.filter(
            deleted=DeletedStatuses.NOT_DELETED.value,
            **params
        ).update(
            deleted=DeletedStatuses.PERMANENTLY_DELETED.value,
        )

        return self._response_success(True)
