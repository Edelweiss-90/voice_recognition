from django.views.generic import TemplateView
from django.conf import settings


class FrontendView(TemplateView):
    template_name = settings.INDEX_PATH
