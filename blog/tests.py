from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from rest_framework_simplejwt.tokens import RefreshToken

from categories.models import Category
from comments.models import Comment
from posts.models import Post

UserModel = get_user_model()


class ApplicationTestBaseClass(APITestCase):
    users: list = []
    categories: list = []
    posts: list = []
    comments: list = []
    users_count: int = 2
    categories_count: int = 50
    posts_count: int = 2
    comments_count: int = 2
    users_password: str = r'user-test-password'
    users_email_pr: str = '@gmail.com'
    user_lookup_url_kwarg: str = 'user_id'
    category_lookup_url_kwarg: str = 'category_id'
    post_lookup_url_kwarg: str = 'post_id'
    comment_lookup_url_kwarg: str = 'comment_id'

    @staticmethod
    def get_token(user: UserModel) -> dict:
        token = RefreshToken.for_user(user)
        return {'HTTP_AUTHORIZATION': f'Bearer {token.access_token}'}

    def setUp(self) -> None:
        self.users = [
            UserModel(username=f'user{index}', email=f'email{index}' + self.users_email_pr,
                      password=self.users_password)
            for index in range(self.users_count)
        ]
        for user in self.users:
            user.save()
        self.categories = [
            Category(title='title '+str(index), owner=self.users[0])
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
        self.comments = [
            Comment(content=str(index), author=self.users[0], post=self.posts[0])
            for index in range(self.comments_count)
        ]
        for comment in self.comments:
            comment.save()
