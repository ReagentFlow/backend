from django.urls import path, include
from rest_framework.routers import DefaultRouter

from reagents.api.views import ContainerModelViewSet, ReagentsViewSet

router = DefaultRouter()
router.register("containers", ContainerModelViewSet, basename="containers")

urlpatterns = [
    path("reagents/", ReagentsViewSet.as_view(), name="reagents"),
    path("", include(router.urls)),
]
