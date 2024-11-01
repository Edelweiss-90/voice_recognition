from django.views.decorators.http import require_POST, require_GET
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from .models import File
from tools import BaseViews, upload_file


class UploaderViews(BaseViews):
    _instance = None
    __model = File

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(UploaderViews, cls).__new__(cls)
        return cls._instance

    @method_decorator(require_POST)
    @method_decorator(login_required)
    def upload(self, request):
        file = request.FILES["file"]
        file_data = upload_file(file)
        self.__model.objects.create(user_id=request.user.id, **file_data)

        return self._response_success('upload')

    @method_decorator(require_POST)
    @method_decorator(login_required)
    def list(self, request):
        result = list(
            self.__model.objects.filter(user_id=request.user.id).values()
            )
        return self._response_success(result)
