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
    invite_code = serializers.CharField(max_length=8, write_only=True)
    re_password = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = User
        fields = (
            "email",
            "password",
            "invite_code",
            "first_name",
            "last_name",
            "middle_name",
            "re_password",
        )

    def create(self, validated_data):
        validated_data.pop("re_password")
        password = validated_data.pop("password")
        invite_code = validated_data.pop("invite_code")

        user = User(**validated_data)
        user.set_password(password)

        try:
            validate_password(password, user)
        except django_exceptions.ValidationError as e:
            serializer_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError({"password": serializer_error[api_settings.NON_FIELD_ERRORS_KEY]})

        user.save()

        invite_code_instance = InviteCode.objects.get(code=invite_code)
        invite_code_instance.code = generate_unique_string(8)
        invite_code_instance.save()

        return user

    def validate(self, attrs):
        code = attrs.get("invite_code", None)

        if not InviteCode.objects.filter(code=code).exists():
            raise serializers.ValidationError({"invite_code": _("Invalid invite code.")})

        password = attrs.get("password", None)
        re_password = attrs.get("re_password", None)

        if password is None or re_password is None or password != re_password:
            raise serializers.ValidationError({"re_password": _("Doesn't match the password.")})

        invite_code = InviteCode.objects.get(code=code)
        attrs["role"] = invite_code.role
        return attrs
