# !/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the  project
# https://github.com/flaminhoe21/corporate-knowledge-managment-vum.git
# author Iva Tsaneva. All rights reserved.

from django.forms.models import inlineformset_factory
from .models import Post, Module
from django import forms

PostsModuleFields = inlineformset_factory(Post, Module, fields=['subject', 'add_desc'], extra=2, can_delete=True)

