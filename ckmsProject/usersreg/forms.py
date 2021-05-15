# !/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the  project
# https://github.com/flaminhoe21/corporate-knowledge-managment-vum.git
# author Iva Tsaneva. All rights reserved.

from django import forms
from publications.models import Post


class PostFollowingForm(forms.Form):
    post_follow_field = forms.ModelChoiceField(queryset=Post.objects.all(), widget=forms.HiddenInput)
