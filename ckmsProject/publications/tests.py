# !/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the  project
# https://github.com/flaminhoe21/corporate-knowledge-managment-vum.git
# author Iva Tsaneva. All rights reserved.

from django.test import TestCase
from .models import Post, Category, Module
from django.contrib.auth.models import User
from model_mommy import mommy
from django.template import Context, Template
from django.urls import reverse, resolve
from .views import PublisherPostList, PublisherPostView

class TestingObjects(TestCase):

    def create_my_object(self, subject="only a test", slug="only_a_test"):
        return Category.objects.create(subject=subject, slug=slug)

    def test_object_creation(self):
        w = self.create_my_object()
        self.assertTrue(isinstance(w, Category))
        self.assertEqual(w.__str__(), w.subject)

class TestPostObject(TestCase):

    def test_post_creation_single(self):
        my_post = mommy.make(Post)
        self.assertTrue(isinstance(my_post, Post))
        self.assertEqual(my_post.__str__(), my_post.subject)

    def test_catetegory(self):
        my_category = mommy.make(Category)
        self.assertTrue(isinstance(my_category, Category))
        self.assertEqual(my_category.__str__(), my_category.subject)

class TestingUrls(TestCase):

    def test_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_posts_detail_url_is_resolved(self):
        url = reverse('posts_list_merge')
        self.assertEquals(resolve(url).func.view_class, PublisherPostList)

    def test_posts_detail_url_is_resolved2(self):
        url = reverse('post_create')
        self.assertEquals(resolve(url).func.view_class, PublisherPostView)
