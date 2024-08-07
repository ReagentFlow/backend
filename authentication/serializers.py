from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from django.utils.translation import gettext_lazy as _
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers
from rest_framework.settings import api_settings

from authentication.models import InviteCode, User
from authentication.utils import generate_unique_string


class InviteCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InviteCode
        fields = (
            "id",
            "code",
            "role",
        )


class UserCreateSerializer(BaseUserCreateSerializer):
    invite_code = serializers.CharField(max_length=8)

    class Meta:
        model = User
        fields = (
            "email",
            "password",
            "invite_code",
            "first_name",
            "last_name",
            "middle_name",
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.pop("invite_code", None)
        return data

    def validate(self, attrs):
        code = attrs.get("invite_code", None)
        if not code:
            raise serializers.ValidationError({"invite_code": _("This field is required.")})
        elif not InviteCode.objects.filter(code=code).exists():
            raise serializers.ValidationError({"invite_code": _("Invalid invite code.")})

        invite_code = InviteCode.objects.get(code=code)
        role = invite_code.role
        attrs["role"] = role
        del attrs["invite_code"]

        invite_code.code = generate_unique_string(8)
        invite_code.save()

        user = User(**attrs)
        password = attrs.get("password")

        try:
            validate_password(password, user)
        except django_exceptions.ValidationError as e:
            serializer_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError({"password": serializer_error[api_settings.NON_FIELD_ERRORS_KEY]})

        return attrs
