from rest_framework import routers

from .views import UpdateInformationViewSet

router = routers.SimpleRouter()
router.register('', UpdateInformationViewSet)
urlpatterns = []

urlpatterns += router.urls
