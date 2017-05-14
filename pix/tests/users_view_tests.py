# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from pix import views
import json

TEST_USER = {'username': 'testuser', 'password': 'dusahb3472 34hruAASD%$!', 'email': 'testuser@lol.com'}


class TestUsersViewNotLoggedIn(TestCase):
    def test_no_access(self):
        rf = RequestFactory()
        request = rf.get('/users/')
        response = views.UsersView.as_view()(request)

        self.assertNotEqual(json.loads(response.content).get('result', None), 'ok')
        self.assertNotEqual(json.loads(response.content).get('users', None), [])

    def test_register(self):
        rf = RequestFactory()
        request = rf.post(
            '/users/',
            TEST_USER
        )
        response = views.UsersView.as_view()(request)

        self.assertEqual(json.loads(response.content).get('result', None), 'ok')
        self.assertEqual(response.status_code, 201)

        u = authenticate(username=TEST_USER['username'], password=TEST_USER['password'])

        self.assertIsNotNone(u)

        u.delete()


class TestUsersViewLoggedIn(TestCase):
    def setUp(self):
        u = User.objects.create(username=TEST_USER.get('username'), email=TEST_USER.get('email'))
        u.set_password(TEST_USER.get('password'))
        u.save()

    def test_see_all_users(self):
        rf = RequestFactory()
        request = rf.get('/users/')
        request.user = User.objects.get(username=TEST_USER['username'])
        response = views.UsersView.as_view()(request)
        self.assertEqual(json.loads(response.content).get('result', None), 'ok')
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        User.objects.get(username=TEST_USER['username']).delete()
