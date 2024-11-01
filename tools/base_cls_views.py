import json
from django.http import JsonResponse


class BaseViews:
    def _loads_data(self, request):
        return json.loads(request.body)

    def _dumps_data(self, data):
        return json.dumps(data)

    def _response_success(self, data):
        return JsonResponse({'success': data})

    def _response_error(self, data):
        return JsonResponse({'error': data})
