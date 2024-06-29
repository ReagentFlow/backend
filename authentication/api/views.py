from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.models import User, InviteCode
from authentication.utils import generate_unique_string


class UserViewSet(DjoserUserViewSet):
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class InviteCodeView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        invite_codes = request.user.invite_codes.all()
        return Response({"codes": [invite_code.code for invite_code in invite_codes]})

    @staticmethod
    def post(request):
        role = request.data.get("role")
        if role not in User.ROLES:
            return Response({"error": "Invalid role"}, status=status.HTTP_400_BAD_REQUEST)
        invite_code = InviteCode.objects.create(code=generate_unique_string(8), role=role, created_by=request.user)
        return Response({"code": invite_code.code}, status=status.HTTP_201_CREATED)
