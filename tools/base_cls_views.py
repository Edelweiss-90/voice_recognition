import json
from django.http import JsonResponse


from .constants import DeletedStatuses
from .exceptions import NotFoundException

class BaseViews:
    def _loads_data(self, request):
        return json.loads(request.body)

    def _dumps_data(self, data):
        return json.dumps(data)

    def _response_success(self, data):
        return JsonResponse({'success': data})

    def _response_error(self, data):
        return JsonResponse({'error': data})

    def _check_exist(self, __model, params: dict[str, int]):
        file = __model.objects.filter(
            deleted=DeletedStatuses.NOT_DELETED.value,
            **params
        ).exists()

        if not file:
            raise NotFoundException()
