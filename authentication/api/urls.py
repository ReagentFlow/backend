from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from authentication.api.views import InviteCodeView


router = DefaultRouter()
router.register('invite_codes/', InviteCodeView, basename='invite_codes')

urlpatterns = [
    path("", include("djoser.urls.jwt")),
    path("", include("djoser.urls")),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("", include(router.urls)),
]
