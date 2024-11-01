from django.apps import AppConfig
from django.conf import settings
import os


class UploaderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'uploader'

    def ready(self):
        path_store = f'{settings.BASE_DIR}/{settings.UPLOAD_DIR}'
        path_tmp = f'{path_store}/{settings.TMP_WAV}'

        if not os.path.isdir(path_store):
            os.mkdir(path_store)
            os.mkdir(path_tmp)
