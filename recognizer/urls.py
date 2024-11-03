from .views import RecognizerViews
from tools import create_urls_and_routers
from django.urls import path

app_name = 'recognizer'
urlpatterns = create_urls_and_routers(RecognizerViews)
