from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from djoser import signals
from djoser.compat import get_user_email
from djoser.conf import settings

from authentication.models import User, InviteCode
from authentication.utils import generate_unique_string

from authentication.serializers import UserCreateSerializer


class UserViewSet(DjoserUserViewSet):
    def perform_create(self, serializer, *args, **kwargs):
        validated_data = serializer.validated_data
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()

        signals.user_registered.send(
            sender=self.__class__, user=user, request=self.request
        )

        context = {"user": user}
        to = [get_user_email(user)]
        if settings.SEND_ACTIVATION_EMAIL:
            settings.EMAIL.activation(self.request, context).send(to)
        elif settings.SEND_CONFIRMATION_EMAIL:
            settings.EMAIL.confirmation(self.request, context).send(to)

    def create(self, request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.validated_data)
        return Response(serializer.validated_data, status=status.HTTP_201_CREATED, headers=headers)


class InviteCodeView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        invite_codes = request.user.invite_codes.all()
        return Response({"invite_codes": [invite_code.code for invite_code in invite_codes]})

    @staticmethod
    def post(request):
        role = request.data.get("role")
        if role not in User.ROLES:
            return Response({"error": "Invalid role"}, status=status.HTTP_400_BAD_REQUEST)
        invite_code = InviteCode.objects.create(code=generate_unique_string(8), role=role, created_by=request.user)
        return Response({"invite_code": invite_code.code}, status=status.HTTP_201_CREATED)
