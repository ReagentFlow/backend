from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.status import HTTP_401_UNAUTHORIZED, HTTP_200_OK, HTTP_201_CREATED, HTTP_403_FORBIDDEN, \
    HTTP_400_BAD_REQUEST

from authentication.models import User
from authentication.serializers import InviteCodeSerializer


class AuthApiTestCase(APITestCase):
    def test_unauthenticated(self):
        url = reverse("auth:users-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)

    def test_token(self):
        user = User(email="root@root.com", password="root", first_name="Root", role="admin")
        user.set_password("root")
        user.save()
        url_token = reverse("auth:token_obtain_pair")
        data = {"email": user.email, "password": "root"}
        response_token = self.client.post(path=url_token, data=data)
        self.assertEqual(response_token.status_code, HTTP_200_OK)

    def test_creating_invite_code(self):
        user = User(email="root@root.com", password="root", first_name="Root", role="admin")
        user.set_password("root")
        user.save()
        url_token = reverse("auth:token_obtain_pair")
        data = {"email": user.email, "password": "root"}
        response_token = self.client.post(path=url_token, data=data)

        token = response_token.data["access"]
        url = reverse("auth:invite_codes")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        response = self.client.post(url, data={"role": "admin"})
        self.assertEqual(response.status_code, HTTP_201_CREATED)

    def test_registration_user(self):
        user = User(email="root@root.com", password="root", first_name="Root", role="admin")
        user.set_password("root")
        user.save()
        url_token = reverse("auth:token_obtain_pair")
        data = {"email": user.email, "password": "root"}
        response_token = self.client.post(path=url_token, data=data)

        token = response_token.data["access"]
        url_invite = reverse("auth:invite_codes")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        response_invite = self.client.post(url_invite, data={"role": "admin"})

        invite_code = InviteCodeSerializer(data=response_invite.data.get("invite_code"))
        invite_code.is_valid()
        code = invite_code.data.get("code")

        url = reverse("auth:users-list")
        data = {
            "email": "user23@gmail.com",
            "password": "lkkksdfj842jA",
            "invite_code": code,
            "first_name": "aba",
            "last_name": "vab",
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, HTTP_201_CREATED)

    def test_permission_user_invite_code(self):
        user = User(email="root@root.com", password="root", first_name="Root", role="admin")
        user.set_password("root")
        user.save()
        url_token = reverse("auth:token_obtain_pair")
        data = {"email": user.email, "password": "root"}
        response_token = self.client.post(path=url_token, data=data)

        token = response_token.data["access"]
        url_invite = reverse("auth:invite_codes")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        response_invite = self.client.post(url_invite, data={"role": "user"})

        invite_code = InviteCodeSerializer(data=response_invite.data.get("invite_code"))
        invite_code.is_valid()
        code = invite_code.data.get("code")

        url_create_user = reverse("auth:users-list")
        data = {
            "email": "user23@gmail.com",
            "password": "lkkksdfj842jA",
            "invite_code": code,
            "first_name": "aba",
            "last_name": "vab",
        }
        response_created = self.client.post(url_create_user, data=data)

        data_login = {"email": data["email"], "password": data["password"]}
        response_token = self.client.post(path=url_token, data=data_login)
        token = response_token.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)

        url = reverse("auth:invite_codes")
        response1 = self.client.get(url)
        post_data1 = {"role": "admin"}
        post_data2 = {"role": "user"}
        response2_1 = self.client.post(url, data=post_data1)
        response2_2 = self.client.post(url, data=post_data2)

        self.assertEqual(response1.status_code, HTTP_403_FORBIDDEN)
        self.assertEqual(response2_1.status_code, HTTP_403_FORBIDDEN)
        self.assertEqual(response2_2.status_code, HTTP_403_FORBIDDEN)

    def test_permissions_admin_invite_code(self):
        user = User(email="root@root.com", password="root", first_name="Root", role="admin")
        user.set_password("root")
        user.save()
        url_token = reverse("auth:token_obtain_pair")
        data = {"email": user.email, "password": "root"}
        response_token = self.client.post(path=url_token, data=data)

        token = response_token.data["access"]
        url_invite = reverse("auth:invite_codes")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        response_invite = self.client.post(url_invite, data={"role": "admin"})

        invite_code = InviteCodeSerializer(data=response_invite.data.get("invite_code"))
        invite_code.is_valid()
        code = invite_code.data.get("code")

        url_create_user = reverse("auth:users-list")
        data = {
            "email": "user23@gmail.com",
            "password": "lkkksdfj842jA",
            "invite_code": code,
            "first_name": "aba",
            "last_name": "vab",
        }
        response_created = self.client.post(url_create_user, data=data)

        data_login = {"email": data["email"], "password": data["password"]}
        response_token = self.client.post(path=url_token, data=data_login)
        token = response_token.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)

        url = reverse("auth:invite_codes")
        response1 = self.client.get(url)
        post_data1 = {"role": "admin"}
        post_data2 = {"role": "user"}
        response2_1 = self.client.post(url, data=post_data1)
        response2_2 = self.client.post(url, data=post_data2)

        self.assertEqual(response1.status_code, HTTP_200_OK)
        self.assertEqual(response2_1.status_code, HTTP_201_CREATED)
        self.assertEqual(response2_2.status_code, HTTP_201_CREATED)

        response3_1 = self.client.post(url, data=post_data2)
        response3_2 = self.client.post(url, data=post_data1)

        self.assertEqual(response3_1.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response3_2.status_code, HTTP_400_BAD_REQUEST)
