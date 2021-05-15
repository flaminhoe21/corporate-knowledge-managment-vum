# !/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the  project
# https://github.com/flaminhoe21/corporate-knowledge-managment-vum.git
# author Iva Tsaneva. All rights reserved.

from django.urls import path
from . import views


urlpatterns = [
    path('mine/',
        views.PublisherPostList.as_view(), name='posts_list_merge'),
    path('create/',
        views.PublisherPostView.as_view(), name='post_create'),
    path('<pk>/edit/',
        views.PublisherPostUpdate.as_view(), name='post_edit'),
    path('<pk>/delete/',
        views.PublisherPostDelete.as_view(), name='post_delete'),
    path('<pk>/module/', views.PostUpdateViewModel.as_view(), name='post_module_update'),

    path('module/<int:module_id>/content/<model_name>/create/',
         views.PostAddContent.as_view(),
         name='module_content_create'),

    path('module/<int:module_id>/content/<model_name>/<id>/',
        views.PostAddContent.as_view(),
        name='module_content_update'),

    path('content/<int:id>/delete/', views.PostContentDelete.as_view(), name='module_content_delete'),

    path('module/<int:module_id>/', views.PostContentListing.as_view(), name='inner_post_list'),

    path('category/<slug:category>/', views.CategoryListing.as_view(), name='categories_listing'),
    path('<slug:slug>/', views.PostDetailsText.as_view(), name='post_details'),

]
