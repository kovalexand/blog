from typing import Any

from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken

from categories.models import Category

UserModel = get_user_model()


class CategoryTestClass(APITestCase):
    users: list = []
    categories: list = []
    users_count: int = 2
    categories_count: int = 2
    users_password: str = r'user-test-password'
    users_email_pr: str = '@gmail.com'
    user_lookup_url_kwarg: str = 'user_id'
    category_lookup_url_kwarg: str = 'category_id'

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
        self.categories = [
            Category(title=str(index), owner=self.users[0])
            for index in range(self.categories_count)
        ]
        for category in self.categories:
            category.save()

    def test_retrieve_category_method(self):
        kwargs = {self.category_lookup_url_kwarg: self.categories[0].pk}
        url = reverse(viewname='categories:category-detail', kwargs=kwargs)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_bad_request_category_method(self):
        kwargs = {self.category_lookup_url_kwarg: None}
        url = reverse(viewname='categories:category-detail', kwargs=kwargs)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_category_method(self):
        url = reverse('categories:category-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_retrieve_category_method(self):
        kwargs = {self.category_lookup_url_kwarg: self.categories[0].pk, self.user_lookup_url_kwarg: self.users[0].pk}
        url = reverse(viewname='categories:user-category-detail', kwargs=kwargs)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_retrieve_bad_request_category_method(self):
        kwargs = {self.category_lookup_url_kwarg: None, self.user_lookup_url_kwarg: None}
        url = reverse(viewname='categories:user-category-detail', kwargs=kwargs)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_list_category_method(self):
        kwargs = {self.user_lookup_url_kwarg: self.users[0].pk}
        url = reverse(viewname='categories:user-category-list', kwargs=kwargs)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_create_category_method(self):
        user = self.users[0]
        kwargs = {self.user_lookup_url_kwarg: user.pk}
        url = reverse(viewname='categories:user-category-list', kwargs=kwargs)
        data = {'title': 'test'}
        token = self.bearer_token(user)
        response = self.client.post(url, data, **token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_no_auth_create_category_method(self):
        user = self.users[0]
        kwargs = {self.user_lookup_url_kwarg: user.pk}
        url = reverse(viewname='categories:user-category-list', kwargs=kwargs)
        data = {'title': 'test'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_create_bad_request_category_method(self):
        user = self.users[0]
        kwargs = {self.user_lookup_url_kwarg: user.pk}
        url = reverse(viewname='categories:user-category-list', kwargs=kwargs)
        data = {'wrong_arg': 'test'}
        token = self.bearer_token(user)
        response = self.client.post(url, data, **token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_permission_user_create_category_method(self):
        user = self.users[0]
        kwargs = {self.user_lookup_url_kwarg: user.pk}
        url = reverse(viewname='categories:user-category-list', kwargs=kwargs)
        data = {'title': 'test'}
        token = self.bearer_token(self.users[1])
        response = self.client.post(url, data, **token)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_update_category_method(self):
        user = self.users[0]
        kwargs = {self.user_lookup_url_kwarg: user.pk, self.category_lookup_url_kwarg: self.categories[0].pk}
        url = reverse(viewname='categories:user-category-detail', kwargs=kwargs)
        data = {'title': 'new_title'}
        token = self.bearer_token(user)
        response = self.client.patch(url, data, **token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.put(url, data, **token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_no_auth_update_category_method(self):
        user = self.users[0]
        kwargs = {self.user_lookup_url_kwarg: user.pk, self.category_lookup_url_kwarg: self.categories[0].pk}
        url = reverse(viewname='categories:user-category-detail', kwargs=kwargs)
        data = {'title': 'new_title'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_another_user_update_category_method(self):
        user = self.users[0]
        kwargs = {self.user_lookup_url_kwarg: user.pk, self.category_lookup_url_kwarg: self.categories[0].pk}
        url = reverse(viewname='categories:user-category-detail', kwargs=kwargs)
        data = {'title': 'new_title'}
        token = self.bearer_token(self.users[1])
        response = self.client.patch(url, data, **token)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.put(url, data, **token)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_bad_request_update_category_method(self):
        user = self.users[0]
        kwargs = {self.user_lookup_url_kwarg: user.pk, self.category_lookup_url_kwarg: self.categories[0].pk}
        url = reverse(viewname='categories:user-category-detail', kwargs=kwargs)
        data = {'wrong_arg': 'new_title'}
        token = self.bearer_token(user)
        response = self.client.patch(url, data, **token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.put(url, data, **token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_delete_category(self):
        user = self.users[0]
        kwargs = {self.user_lookup_url_kwarg: user.pk, self.category_lookup_url_kwarg: self.categories[0].pk}
        url = reverse(viewname='categories:user-category-detail', kwargs=kwargs)
        token = self.bearer_token(user)
        response = self.client.delete(url, **token)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_another_user_delete_category(self):
        user = self.users[0]
        kwargs = {self.user_lookup_url_kwarg: user.pk, self.category_lookup_url_kwarg: self.categories[0].pk}
        url = reverse(viewname='categories:user-category-detail', kwargs=kwargs)
        token = self.bearer_token(self.users[1])
        response = self.client.delete(url, **token)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
