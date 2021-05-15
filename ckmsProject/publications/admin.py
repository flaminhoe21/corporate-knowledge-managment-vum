# !/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the  project
# https://github.com/flaminhoe21/corporate-knowledge-managment-vum.git
# author Iva Tsaneva. All rights reserved.

from django.contrib import admin
from .models import Category, Post, Module


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    showing_elements = ['subject', 'slug']
    fields_structured = {'slug': ('subject',)}


class ModuleInline(admin.StackedInline):
    model = Module


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    showing_elements = ['subject', 'category', 'published']
    filtering_elements = ['published', 'category']
    fields_src = ['subject', 'overview']
    fields_structured = {'slug': ('subject',)}
    oneline = [ModuleInline]
