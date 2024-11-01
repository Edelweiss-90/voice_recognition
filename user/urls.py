from .views import UserViews
from tools import create_urls_and_routers

urlpatterns = create_urls_and_routers(UserViews)
