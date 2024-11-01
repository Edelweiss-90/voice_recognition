from django.views.decorators.http import require_POST, require_GET
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from .models import File
from tools import (
    BaseViews,
    upload_file,
    id_validator,
    DeletedStatuses,
    file_validation,
    NotFoundException,
    handle_validation_errors
    )


class UploaderViews(BaseViews):
    _instance = None
    __model = File

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
        print(file_data)
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
        params = (id, request.user.id)

        file = self.__model.objects.filter(*params).exists()

        if not file:
            raise NotFoundException()

        file = self.__model.objects.get(*params)

        return self._response_success({
            'id': file.id,
            'title': file.title,
            'size': file.size,
            'created_at': file.created_at
        })
