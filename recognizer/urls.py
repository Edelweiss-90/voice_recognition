from .views import RecognizerViews
from tools import create_urls_and_routers
from django.urls import path

urlpatterns = create_urls_and_routers(RecognizerViews, '/<int:id>/')
