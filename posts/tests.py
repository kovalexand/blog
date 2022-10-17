from typing import Any

from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken

from categories.models import Category
from posts.models import Post

UserModel = get_user_model()


class CategoryTestClass(APITestCase):
    users: list = []
    categories: list = []
    posts: list = []
    users_count: int = 2
    categories_count: int = 2
    posts_count: int = 2
    users_password: str = r'user-test-password'
    users_email_pr: str = '@gmail.com'
    user_lookup_url_kwarg: str = 'user_id'
    category_lookup_url_kwarg: str = 'category_id'
    post_lookup_url_kwarg: str = 'post_id'

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
        self.posts = [
            Post(title=str(index), content=str(index), owner=self.users[0], category=self.categories[0])
            for index in range(self.posts_count)
        ]
        for post in self.posts:
            post.save()

    def test_retrieve_post_method(self):
        kwargs = {self.post_lookup_url_kwarg: self.posts[0].pk}
        url = reverse(viewname='posts:post-detail', kwargs=kwargs)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_bad_request_method(self):
        kwargs = {self.post_lookup_url_kwarg: None}
        url = reverse(viewname='posts:post-detail', kwargs=kwargs)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_category_list_post_method(self):
        kwargs = {self.category_lookup_url_kwarg: self.categories[0].pk}
        url = reverse(viewname='posts:category-post-list', kwargs=kwargs)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_category_retrieve_post_method(self):
        kwargs = {self.category_lookup_url_kwarg: self.categories[0].pk, self.post_lookup_url_kwarg: self.posts[0].pk}
        url = reverse(viewname='posts:category-post-detail', kwargs=kwargs)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_category_retrieve_bad_request_post_method(self):
        kwargs = {self.category_lookup_url_kwarg: None, self.post_lookup_url_kwarg: None}
        url = reverse(viewname='posts:category-post-detail', kwargs=kwargs)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_list_post_method(self):
        kwargs = {self.user_lookup_url_kwarg: self.users[0].pk}
        url = reverse(viewname='posts:user-post-list', kwargs=kwargs)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_retrieve_post_method(self):
        kwargs = {self.user_lookup_url_kwarg: self.users[0].pk, self.post_lookup_url_kwarg: self.posts[0].pk}
        url = reverse(viewname='posts:user-post-detail', kwargs=kwargs)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_retrieve_bad_request_post_method(self):
        kwargs = {self.user_lookup_url_kwarg: None, self.post_lookup_url_kwarg: None}
        url = reverse(viewname='posts:user-post-detail', kwargs=kwargs)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_category_list_post_method(self):
        kwargs = {self.user_lookup_url_kwarg: self.users[0].pk, self.category_lookup_url_kwarg: self.categories[0].pk}
        url = reverse(viewname='posts:user-category-post-list', kwargs=kwargs)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_category_retrieve_post_method(self):
        kwargs = {
            self.user_lookup_url_kwarg: self.users[0].pk,
            self.category_lookup_url_kwarg: self.categories[0].pk,
            self.post_lookup_url_kwarg: self.posts[0].pk
        }
        url = reverse(viewname='posts:user-category-post-detail', kwargs=kwargs)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_category_create_post_method(self):
        kwargs = {self.user_lookup_url_kwarg: self.users[0].pk, self.category_lookup_url_kwarg: self.categories[0].pk}
        url = reverse(viewname='posts:user-category-post-list', kwargs=kwargs)
        token = self.bearer_token(self.users[0])
        data = {'title': 'test', 'content': 'test'}
        response = self.client.post(url, data, **token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_category_delete_post_method(self):
        kwargs = {
            self.user_lookup_url_kwarg: self.users[0].pk,
            self.category_lookup_url_kwarg: self.categories[0].pk,
            self.post_lookup_url_kwarg: self.posts[0].pk
        }
        url = reverse(viewname='posts:user-category-post-detail', kwargs=kwargs)
        token = self.bearer_token(self.users[0])
        response = self.client.delete(url, **token)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_category_update_post_method(self):
        kwargs = {
            self.user_lookup_url_kwarg: self.users[0].pk,
            self.category_lookup_url_kwarg: self.categories[0].pk,
            self.post_lookup_url_kwarg: self.posts[0].pk
        }
        url = reverse(viewname='posts:user-category-post-detail', kwargs=kwargs)
        token = self.bearer_token(self.users[0])
        data = {'title': 'test', 'content': 'test'}
        response = self.client.patch(url, data, **token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.put(url, data, **token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
