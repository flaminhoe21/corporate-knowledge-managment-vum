# !/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the  project
# https://github.com/flaminhoe21/corporate-knowledge-managment-vum.git
# author Iva Tsaneva. All rights reserved.

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm


class BaseTest(TestCase):
    def setUp(self):
        self.register_url=reverse('user_register')
        return super().setUp()


class RegisterTest(BaseTest):

    def test_view_page_correctly(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/user/register_user.html')


class UserCreationFormTest(TestCase):

    def test_form(self):
        data = {
            'username': 'testuser',
            'password1': 'Test_12345',
            'password2': 'Test_12345',
        }

        form = UserCreationForm(data)
        self.assertTrue(form.is_valid(),)
        self.assertTrue(form.is_valid(),)

