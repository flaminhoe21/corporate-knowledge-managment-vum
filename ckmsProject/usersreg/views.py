# !/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the  project
# https://github.com/flaminhoe21/corporate-knowledge-managment-vum.git
# author Iva Tsaneva. All rights reserved.

from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PostFollowingForm
from django.views.generic.list import ListView
from publications.models import Post
from django.views.generic.detail import DetailView


class UsersRegistrationView(CreateView):
    template_name = 'users/user/register_user.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('users_posts_listing')

    def form_valid(self, form):
        new_user_reg = super().form_valid(form)
        clean_data = form.cleaned_data
        user = authenticate(username=clean_data['username'], password=clean_data['password1'])
        login(self.request, user)
        return new_user_reg


class UserFollowingAPostView(LoginRequiredMixin, FormView):
    post_follow_field = None
    form_class = PostFollowingForm

    def form_valid(self, form):
        self.post_follow_field = form.cleaned_data['post_follow_field']
        self.post_follow_field.users_follow.add(self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('details_user_publications', args=[self.post_follow_field.id])


class UsersPostsListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'users/post/listing_posts.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(users_follow__in=[self.request.user])


class UserPostDetailView(DetailView):
    model = Post
    template_name = 'users/post/detail_posts.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(users_follow__in=[self.request.user])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_follow_field = self.get_object()
        if 'module_id' in self.kwargs:
            context['module'] = post_follow_field.modules.get(id=self.kwargs['module_id'])
        else:
            context['module'] = post_follow_field.modules.all()[0]
        return context

