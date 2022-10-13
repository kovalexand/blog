from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken

UserModel = get_user_model()


class UserPermissionTestClass(APITestCase):
    first_user_email: str = "ftest@gmail.com"
    first_user_password: str = "password"
    first_user_username: str = "username"
    second_user_email: str = "stest@gmail.com"
    second_user_password: str = "password"
    second_user_username: str = "username"
    user_detail_view: str = 'users:user-detail'
    lookup_url_kwarg: str = "user_id"

    @staticmethod
    def bearer_token(email: str) -> dict:
        user = UserModel.objects.get(email=email)
        refresh = RefreshToken.for_user(user)
        return {"HTTP_AUTHORIZATION": f'Bearer {refresh.access_token}'}

    def setUp(self) -> None:
        first_user = UserModel.objects.create_user(
            email=self.first_user_email, password=self.first_user_password, username=self.first_user_username
        )
        second_user = UserModel.objects.create_user(
            email=self.second_user_email, password=self.second_user_password, username=self.second_user_username
        )
        first_user.save()
        second_user.save()

    def test_delete_user_by_another_user(self):
        first_user = UserModel.objects.get(email=self.first_user_email)
        second_user = UserModel.objects.get(email=self.second_user_email)
        data = {self.lookup_url_kwarg: first_user.pk}
        user_detail_url = reverse(viewname=self.user_detail_view, kwargs=data)
        token = self.bearer_token(second_user.email)
        response = self.client.delete(user_detail_url, **token)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_user_by_current_user(self):
        first_user = UserModel.objects.get(email=self.first_user_email)
        data = {self.lookup_url_kwarg: first_user.pk}
        user_detail_url = reverse(viewname=self.user_detail_view, kwargs=data)
        token = self.bearer_token(first_user.email)
        response = self.client.delete(user_detail_url, **token)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
