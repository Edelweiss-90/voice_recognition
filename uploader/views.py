from django.views.decorators.http import require_POST, require_GET
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db import transaction

from models import File, Recognizer
from tools import (
    BaseViews,
    DeletedStatuses,
    upload_file,
    id_validator,
    id_params_validator,
    file_validation,
    NotFoundException,
    handle_validation_errors
    )


class UploaderViews(BaseViews):
    _instance = None
    __model = File
    __recognizer = Recognizer

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(UploaderViews, cls).__new__(cls)
        return cls._instance

    @method_decorator(require_POST)
    @method_decorator(login_required)
    @handle_validation_errors
    @file_validation
    def upload(self, request):
        file = request.FILES.get('file')
        file_data = upload_file(file)
        self.__model.objects.create(user_id=request.user.id, **file_data)

        return self._response_success('upload')

    @method_decorator(require_GET)
    @method_decorator(login_required)
    def list(self, request):

        files = self.__model.objects.filter(
            user_id=request.user.id,
            deleted=DeletedStatuses.NOT_DELETED.name
        )

        return self._response_success([
            {
                'id': file.id,
                'title': file.title,
                'size': file.size,
                'created_at': file.created_at
            }
            for file in files
        ])

    @method_decorator(require_GET)
    @method_decorator(login_required)
    @handle_validation_errors
    @id_validator
    def file_by_id(self, request, id):
        params = {
            'id': id,
            'user_id': request.user.id
        }

        self._check_exist(self.__model, params)

        file = self.__model.objects.get(**params)

        return self._response_success({
            'id': file.id,
            'title': file.title,
            'size': file.size,
            'created_at': file.created_at
        })

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

        self.__model.objects.filter(**params).update(
            deleted=DeletedStatuses.PERMANENTLY_DELETED.value,
        )

        self.__recognizer.objects.filter(
            deleted=DeletedStatuses.NOT_DELETED.value,
            file_id=params['id']
        ).update(
            deleted=DeletedStatuses.CASCADE_DELETED.value,
        )

        return self._response_success(True)
