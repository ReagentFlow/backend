from django.db.models import QuerySet
from djoser import signals
from djoser.compat import get_user_email
from djoser.conf import settings
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.api.permissions import IsAuthenticatedAndAdmin
from authentication.models import InviteCode, User
from authentication.serializers import InviteCodeSerializer, UserCreateSerializer
from authentication.utils import generate_unique_string


class UserViewSet(DjoserUserViewSet):

    def get_queryset(self):
        user = self.request.user

        queryset = self.queryset
        if isinstance(queryset, QuerySet):
            queryset = queryset.all()

        if settings.HIDE_USERS and self.action == "list" and user.role == User.USER:
            queryset = queryset.filter(pk=user.pk)

        return queryset

    def perform_create(self, serializer, *args, **kwargs):
        user = serializer.save(*args, **kwargs)

        signals.user_registered.send(sender=self.__class__, user=user, request=self.request)

        context = {"user": user}
        to = [get_user_email(user)]
        if settings.SEND_ACTIVATION_EMAIL:
            settings.EMAIL.activation(self.request, context).send(to)
        elif settings.SEND_CONFIRMATION_EMAIL:
            settings.EMAIL.confirmation(self.request, context).send(to)

        return user

    @staticmethod
    def create_invite_codes(user):
        admin_code = generate_unique_string(8)
        user_code = generate_unique_string(8)
        InviteCode.objects.create(created_by=user, code=admin_code, role="user")
        InviteCode.objects.create(created_by=user, code=user_code, role="admin")

    def create(self, request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance_user = self.perform_create(serializer)

        if instance_user.role == "admin":
            self.create_invite_codes(instance_user)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class InviteCodeView(APIView):
    permission_classes = [IsAuthenticatedAndAdmin]

    @staticmethod
    def get(request):
        invite_codes = request.user.invite_codes.all()
        serializer = InviteCodeSerializer(invite_codes, many=True)
        return Response({"invite_codes": [invite_code for invite_code in serializer.data]})

    @staticmethod
    def post(request):
        role = request.data.get("role")
        if role not in User.ROLES.values():
            return Response({"error": "Invalid role"}, status=status.HTTP_400_BAD_REQUEST)
        elif InviteCode.objects.filter(role=role, created_by=request.user).exists():
            return Response(
                {"error": "You already have an active invite code for this role"}, status=status.HTTP_400_BAD_REQUEST
            )
        invite_code = InviteCode.objects.create(code=generate_unique_string(8), role=role, created_by=request.user)
        serializer = InviteCodeSerializer(invite_code)
        return Response({"invite_code": serializer.data}, status=status.HTTP_201_CREATED)
