from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Post
from . import views

# Create your tests here.
class PostTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.user = User.objects.create_user(username='bob_user_tester',
                                        password='qwerty')
        cls.first = Post.objects.create(user=cls.user, title='first', content='abc')
        cls.second = Post.objects.create(user=cls.user, title='sec', content='def')
        cls.third = Post.objects.create(user=cls.user, title='third', content='ewww')
        cls.fourth = Post.objects.create(user=cls.user, title='fourth', content='fgh')
        cls.fifth = Post.objects.create(user=cls.user, title='fifth', content='vc')
        cls.sixth = Post.objects.create(user=cls.user, title='sixth', content='tttt')
        cls.root_response = cls.client.get('/')

    def test_root_status_code(self):
        self.assertEqual(self.root_response.status_code, 200)

    def test_visiting_root_resolves_home_view(self):
        self.assertEqual(self.root_response.resolver_match.func, views.home)

    def test_home_paginator(self):
        self.assertContains(self.root_response, 'sixth')
        self.assertContains(self.root_response, 'sec')
        self.assertNotContains(self.root_response, 'first')

    def test_post_creation_anonymous_user_get_method(self):
        response = self.client.get('/create/')
        self.assertEqual(response.status_code, 302)

    def test_post_creation_anonymous_user_post_method(self):
        response = self.client.post('/create/', {'title': 'xd', 'content': 'f'})
        self.assertEqual(response.status_code, 302)
        self.assertRaises(Post.DoesNotExist, Post.objects.get, title='xd')

    def test_post_creation_logged_user_get_method(self):
        self.client.login(username='bob_user_tester', password='qwerty')
        response = self.client.get('/create/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func, views.create)
        self.assertContains(response, '<form')

    def test_post_creation_logged_user_post_method(self):
        self.client.login(username='bob_user_tester', password='qwerty')
        response = self.client.post('/create/', {'title': 'ab', 'content': 'z'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.resolver_match.func, views.create)
        try:
            Post.objects.get(title='ab')
        except Post.DoesNotExist as exc:
            self.fail(exc)

        self.assertEqual(Post.objects.get(title='ab').user.username,
                                         'bob_user_tester' )
