from django.views.generic import TemplateView
from django.conf import settings


class FrontendView(TemplateView):
    print(settings.INDEX_PATH)
    template_name = settings.INDEX_PATH
