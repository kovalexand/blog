from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from blog.tests import ApplicationTestBaseClass

UserModel = get_user_model()


class CategoryTestClass(ApplicationTestBaseClass):
    def test_retrieve_category_with_query_method(self):
        kwargs = {self.category_lookup_url_kwarg: self.categories[0].pk}
        url = '%s?title=title' % reverse(viewname='category-detail', kwargs=kwargs)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_category_method(self):
        kwargs = {self.category_lookup_url_kwarg: self.categories[0].pk}
        url = reverse(viewname='category-detail', kwargs=kwargs)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_bad_request_category_method(self):
        kwargs = {self.category_lookup_url_kwarg: None}
        url = reverse(viewname='category-detail', kwargs=kwargs)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_category_method(self):
        url = reverse('category-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_retrieve_category_method(self):
        kwargs = {self.category_lookup_url_kwarg: self.categories[0].pk, self.user_lookup_url_kwarg: self.users[0].pk}
        url = reverse(viewname='user-category-detail', kwargs=kwargs)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_retrieve_bad_request_category_method(self):
        kwargs = {self.category_lookup_url_kwarg: None, self.user_lookup_url_kwarg: None}
        url = reverse(viewname='user-category-detail', kwargs=kwargs)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_list_category_method(self):
        kwargs = {self.user_lookup_url_kwarg: self.users[0].pk}
        url = reverse(viewname='user-category-list', kwargs=kwargs)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_create_category_method(self):
        user = self.users[0]
        kwargs = {self.user_lookup_url_kwarg: user.pk}
        url = reverse(viewname='user-category-list', kwargs=kwargs)
        data = {'title': 'test'}
        token = self.get_token(user)
        response = self.client.post(url, data, **token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_no_auth_create_category_method(self):
        user = self.users[0]
        kwargs = {self.user_lookup_url_kwarg: user.pk}
        url = reverse(viewname='user-category-list', kwargs=kwargs)
        data = {'title': 'test'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_create_bad_request_category_method(self):
        user = self.users[0]
        kwargs = {self.user_lookup_url_kwarg: user.pk}
        url = reverse(viewname='user-category-list', kwargs=kwargs)
        data = {'wrong_arg': 'test'}
        token = self.get_token(user)
        response = self.client.post(url, data, **token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_permission_user_create_category_method(self):
        user = self.users[0]
        kwargs = {self.user_lookup_url_kwarg: user.pk}
        url = reverse(viewname='user-category-list', kwargs=kwargs)
        data = {'title': 'test'}
        token = self.get_token(self.users[1])
        response = self.client.post(url, data, **token)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_update_category_method(self):
        user = self.users[0]
        kwargs = {self.user_lookup_url_kwarg: user.pk, self.category_lookup_url_kwarg: self.categories[0].pk}
        url = reverse(viewname='user-category-detail', kwargs=kwargs)
        data = {'title': 'new_title'}
        token = self.get_token(user)
        response = self.client.patch(url, data, **token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.put(url, data, **token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_no_auth_update_category_method(self):
        user = self.users[0]
        kwargs = {self.user_lookup_url_kwarg: user.pk, self.category_lookup_url_kwarg: self.categories[0].pk}
        url = reverse(viewname='user-category-detail', kwargs=kwargs)
        data = {'title': 'new_title'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_another_user_update_category_method(self):
        user = self.users[0]
        kwargs = {self.user_lookup_url_kwarg: user.pk, self.category_lookup_url_kwarg: self.categories[0].pk}
        url = reverse(viewname='user-category-detail', kwargs=kwargs)
        data = {'title': 'new_title'}
        token = self.get_token(self.users[1])
        response = self.client.patch(url, data, **token)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.put(url, data, **token)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_bad_request_update_category_method(self):
        user = self.users[0]
        kwargs = {self.user_lookup_url_kwarg: user.pk, self.category_lookup_url_kwarg: self.categories[0].pk}
        url = reverse(viewname='user-category-detail', kwargs=kwargs)
        data = {'wrong_arg': 'new_title'}
        token = self.get_token(user)
        response = self.client.patch(url, data, **token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.put(url, data, **token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_delete_category(self):
        user = self.users[0]
        kwargs = {self.user_lookup_url_kwarg: user.pk, self.category_lookup_url_kwarg: self.categories[0].pk}
        url = reverse(viewname='user-category-detail', kwargs=kwargs)
        token = self.get_token(user)
        response = self.client.delete(url, **token)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_another_user_delete_category(self):
        user = self.users[0]
        kwargs = {self.user_lookup_url_kwarg: user.pk, self.category_lookup_url_kwarg: self.categories[0].pk}
        url = reverse(viewname='user-category-detail', kwargs=kwargs)
        token = self.get_token(self.users[1])
        response = self.client.delete(url, **token)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
