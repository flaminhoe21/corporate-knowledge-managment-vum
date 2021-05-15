# !/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the  project
# https://github.com/flaminhoe21/corporate-knowledge-managment-vum.git
# author Iva Tsaneva. All rights reserved.

from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from .fields import OrderField
from django.template.loader import render_to_string


class Category(models.Model):
    subject = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['subject']

    def __str__(self):
        return self.subject


class Post(models.Model):
    publisher = models.ForeignKey(User, related_name='posts_published', on_delete=models.CASCADE)

    category = models.ForeignKey(Category, related_name='posts', on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    overview = models.TextField()
    published = models.DateTimeField(auto_now_add=True)
    users_follow = models.ManyToManyField(User, related_name='post_follow', blank=True)

    class Meta:
        ordering = ['-published']

    def __str__(self):
        return self.subject


class Module(models.Model):
    post = models.ForeignKey(Post, related_name='modules', on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    add_desc = models.TextField(blank=True)
    order = OrderField(blank=True, for_fields=['post'])

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.order}. {self.subject}'


class Content(models.Model):
    module = models.ForeignKey(Module, related_name='contents', on_delete=models.CASCADE)
    inner_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,
                                            limit_choices_to={'model__in': (
                                            'text',
                                            'video',
                                            'image',
                                            'file')})
    item_id = models.PositiveIntegerField()
    item = GenericForeignKey('inner_content_type', 'item_id')
    order = OrderField(blank=True, for_fields=['module'])

    class Meta:
        ordering = ['order']


class MainStructureItems(models.Model):
    publisher = models.ForeignKey(User, related_name='%(class)s_related', on_delete=models.CASCADE)
    subject = models.CharField(max_length=250)
    published = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.subject

    def render(self):
        return render_to_string(
            f'publications/content/{self._meta.model_name}.html',
            {'item': self})


class FileText(MainStructureItems):
    content = models.TextField()


class OnlyFile(MainStructureItems):
    file = models.FileField(upload_to='files')


class FileImage(MainStructureItems):
    image = models.FileField(upload_to='images')


class FileVideo(MainStructureItems):
    url = models.URLField()

