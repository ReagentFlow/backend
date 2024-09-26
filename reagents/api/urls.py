from django.urls import include, path
from rest_framework.routers import DefaultRouter

from reagents.api.views import ContainerModelViewSet, ReagentsViewSet, get_container_barcode_pdf

router = DefaultRouter()
router.register("containers", ContainerModelViewSet, basename="containers")

urlpatterns = [
    path("generate-pdf/<str:container_id>/", get_container_barcode_pdf, name="generate_pdf_with_barcode"),
    path("reagents/", ReagentsViewSet.as_view(), name="reagents"),
    path("", include(router.urls)),
]
