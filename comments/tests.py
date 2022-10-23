from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from blog.tests import ApplicationTestBaseClass

UserModel = get_user_model()


class CommentsTestClass(ApplicationTestBaseClass):
    def test_retrieve_comment_method(self):
        kwargs = {self.comment_lookup_url_kwarg: self.comments[0].pk}
        url = reverse(viewname='comment-detail', kwargs=kwargs)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_list_comment_method(self):
        kwargs = {self.post_lookup_url_kwarg: self.posts[0].pk}
        url = reverse(viewname='post-comment-list', kwargs=kwargs)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_retrieve_comment_method(self):
        kwargs = {self.post_lookup_url_kwarg: self.posts[0].pk, self.comment_lookup_url_kwarg: self.comments[0].pk}
        url = reverse(viewname='post-comment-detail', kwargs=kwargs)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_list_comment_method(self):
        kwargs = {self.user_lookup_url_kwarg: self.users[0].pk}
        url = reverse(viewname='user-comment-list', kwargs=kwargs)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_retrieve_comment_method(self):
        kwargs = {self.user_lookup_url_kwarg: self.users[0].pk, self.comment_lookup_url_kwarg: self.comments[0].pk}
        url = reverse(viewname='user-comment-detail', kwargs=kwargs)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_post_list_comment_method(self):
        kwargs = {self.user_lookup_url_kwarg: self.users[0].pk, self.post_lookup_url_kwarg: self.posts[0].pk}
        url = reverse(viewname='user-post-comment-list', kwargs=kwargs)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_post_retrieve_comment_method(self):
        kwargs = {
            self.user_lookup_url_kwarg: self.users[0].pk,
            self.post_lookup_url_kwarg: self.posts[0].pk,
            self.comment_lookup_url_kwarg: self.comments[0].pk
        }
        url = reverse(viewname='user-post-comment-detail', kwargs=kwargs)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_post_delete_comment_method(self):
        kwargs = {
            self.user_lookup_url_kwarg: self.users[0].pk,
            self.post_lookup_url_kwarg: self.posts[0].pk,
            self.comment_lookup_url_kwarg: self.comments[0].pk
        }
        url = reverse(viewname='user-post-comment-detail', kwargs=kwargs)
        token = self.get_token(self.users[0])
        response = self.client.delete(url, **token)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_post_update_comment_method(self):
        kwargs = {
            self.user_lookup_url_kwarg: self.users[0].pk,
            self.post_lookup_url_kwarg: self.posts[0].pk,
            self.comment_lookup_url_kwarg: self.comments[0].pk
        }
        url = reverse(viewname='user-post-comment-detail', kwargs=kwargs)
        token = self.get_token(self.users[0])
        data = {'content': 'test'}
        response = self.client.put(url, data, **token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.patch(url, data, **token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_post_create_comment_method(self):
        kwargs = {self.user_lookup_url_kwarg: self.users[0].pk, self.post_lookup_url_kwarg: self.posts[0].pk}
        url = reverse(viewname='user-post-comment-list', kwargs=kwargs)
        token = self.get_token(self.users[0])
        data = {'content': 'test'}
        response = self.client.post(url, data, **token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
