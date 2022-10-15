from typing import Any

from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken

UserModel = get_user_model()


class UsersTestClass(APITestCase):
    users: list = []
    users_count: int = 2
    users_password: str = r'user-test-password'
    users_email_pr: str = '@gmail.com'
    user_lookup_url_kwarg: str = 'user_id'

    @staticmethod
    def bearer_token(user: Any) -> dict:
        token = RefreshToken.for_user(user)
        return {'HTTP_AUTHORIZATION': f'Bearer {token.access_token}'}

    def setUp(self) -> None:
        self.users = [
            UserModel(username=f'user{index}', email=f'email{index}'+self.users_email_pr, password=self.users_password)
            for index in range(self.users_count)
        ]
        for user in self.users:
            user.save()

    def test_retrieve_user_method(self):
        kwargs = {self.user_lookup_url_kwarg: self.users[0].pk}
        url = reverse(viewname='users:user-detail', kwargs=kwargs)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_bad_request_user_method(self):
        kwargs = {self.user_lookup_url_kwarg: None}
        url = reverse(viewname='users:user-detail', kwargs=kwargs)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_user_method(self):
        url = reverse('users:user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_user_method(self):
        url = reverse('users:user-list')
        data = {'email': 'test'+self.users_email_pr, 'password': self.users_password, 'username': 'test'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_already_exist_user_method(self):
        url = reverse('users:user-list')
        user = self.users[0]
        data = {'email': user.email, 'password': user.password, 'username': user.username}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_user_method(self):
        user = self.users[0]
        kwargs = {self.user_lookup_url_kwarg: user.pk}
        url = reverse(viewname='users:user-detail', kwargs=kwargs)
        data = {'password': 'new_password'}
        token = self.bearer_token(user)
        response = self.client.patch(url, data, **token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = {'email': user.email, 'password': user.password, 'username': user.username}
        response = self.client.put(url, data, **token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_by_another_user_method(self):
        user = self.users[0]
        kwargs = {self.user_lookup_url_kwarg: user.pk}
        url = reverse(viewname='users:user-detail', kwargs=kwargs)
        data = {'password': 'new_password'}
        token = self.bearer_token(self.users[1])
        response = self.client.patch(url, data, **token)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        data = {'email': user.email, 'password': user.password, 'username': user.username}
        response = self.client.put(url, data, **token)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_user_method(self):
        user = self.users[0]
        kwargs = {self.user_lookup_url_kwarg: user.pk}
        url = reverse(viewname='users:user-detail', kwargs=kwargs)
        token = self.bearer_token(user)
        response = self.client.delete(url, **token)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_user_by_another_user_method(self):
        user = self.users[0]
        kwargs = {self.user_lookup_url_kwarg: user.pk}
        url = reverse(viewname='users:user-detail', kwargs=kwargs)
        token = self.bearer_token(self.users[1])
        response = self.client.delete(url, **token)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
