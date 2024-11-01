from django.http import JsonResponse
import os
from django.conf import settings

from tools import MemorySizes



class FileSizeMiddleware:

    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def __call__(self, request):
        if 'upload' in request.path and request.FILES:

            file = request.FILES.get('file')
            file_destination = os.path.splitext(file.name)

            if file_destination[1] not in settings.EXTENSIONS:
                return JsonResponse({
                    'error': 'not supported format'
                    }, status=400)

            if file and file.size > MemorySizes.ONE_GB.value:
                return JsonResponse({
                    'error': 'File size exceeds 1 GB limit'
                    }, status=400)

        return self.get_response(request)
