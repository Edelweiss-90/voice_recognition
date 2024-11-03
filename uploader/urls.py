from .views import UploaderViews
from tools import create_urls_and_routers

app_name = 'uploader'
urlpatterns = create_urls_and_routers(UploaderViews)
