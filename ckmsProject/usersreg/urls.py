# !/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the  project
# https://github.com/flaminhoe21/corporate-knowledge-managment-vum.git
# author Iva Tsaneva. All rights reserved.

from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.UsersRegistrationView.as_view(), name='user_register'),
    path('follow-post/', views.UserFollowingAPostView.as_view(), name='user_following_posts'),

    path('posts/', views.UsersPostsListView.as_view(), name='users_posts_listing'),
    path('post/<pk>/', views.UserPostDetailView.as_view(), name='details_user_publications'),
    path('post/<pk>/<module_id>/', views.UserPostDetailView.as_view(), name='users_posts_details_module'),

]