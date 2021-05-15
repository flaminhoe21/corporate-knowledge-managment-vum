# !/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the  project
# https://github.com/flaminhoe21/corporate-knowledge-managment-vum.git
# author Iva Tsaneva. All rights reserved. 

from .models import Post
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.views.generic.base import TemplateResponseMixin, View
from .forms import PostsModuleFields
from django.forms.models import modelform_factory
from django.apps import apps
from .models import Module, Content
from django.db.models import Count
from .models import Category
from django.views.generic.detail import DetailView
from usersreg.forms import PostFollowingForm


class PublisherMerge(object):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(publisher=self.request.user)


class PublisherEditMerge(object):
    def form_valid(self, form):
        form.instance.publisher = self.request.user
        return super().form_valid(form)


class PublisherPostMerge(PublisherMerge, LoginRequiredMixin, PermissionRequiredMixin):
    model = Post
    fields = ['category', 'subject', 'slug', 'overview']
    success_url = reverse_lazy('posts_list_merge')


class PublisherPostEdit(PublisherPostMerge, PublisherEditMerge):
    template_name = 'publications/manage/post/form.html'


class PublisherPostList(PublisherPostMerge, ListView):
    template_name = 'publications/manage/post/list.html'
    permission_required = 'publications.view_post'


class PublisherPostView(PublisherPostEdit, CreateView):
    permission_required = 'publications.add_post'


class PublisherPostUpdate(PublisherPostEdit, UpdateView):
    permission_required = 'publications.change_post'


class PublisherPostDelete(PublisherPostMerge, DeleteView):
    template_name = 'publications/manage/post/delete.html'
    permission_required = 'publications.delete_post'


class PostUpdateViewModel(TemplateResponseMixin, View):
    template_name = 'publications/manage/module/formset.html'
    object = None

    def get_formset(self, data=None):
        return PostsModuleFields(instance=self.object, data=data)

    def dispatch(self, request, pk):
        self.object = get_object_or_404(Post, id=pk, publisher=request.user)
        return super().dispatch(request, pk)

    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({'post': self.object, 'formset': formset})

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('posts_list_merge')
        return self.render_to_response({'post': self.object, 'formset': formset})


class PostAddContent(TemplateResponseMixin, View):
    module = None
    model = None
    obj = None
    template_name = 'publications/manage/content/form.html'

    def get_model(self, model_name):
        if model_name in ['filetext', 'filevideo', 'fileimage', 'onlyfile']:
            return apps.get_model(app_label='publications', model_name=model_name)
        return None

    def get_form(self, model, *args, **kwargs):
        Form = modelform_factory(model, exclude=['publisher', 'order', 'published', 'updated'])
        return Form(*args, **kwargs)

    def dispatch(self, request, module_id, model_name, id=None):
        self.module = get_object_or_404(Module, id=module_id, post__publisher=request.user)
        self.model = self.get_model(model_name)
        if id:
            self.obj = get_object_or_404(self.model, id=id, publisher=request.user)
        return super().dispatch(request, module_id, model_name, id)

    def get(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model, instance=self.obj)

        return self.render_to_response({'form': form, 'object': self.obj})

    def post(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model, instance=self.obj, data=request.POST, files=request.FILES)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.publisher = request.user
            obj.save()
            if not id:

                Content.objects.create(module=self.module, item=obj)

            return redirect('inner_post_list', self.module.id)
        return self.render_to_response({'form': form, 'object': self.obj})


class PostContentDelete(View):

    def post(self, request, id):
        content = get_object_or_404(Content, id=id, module__post__publisher=request.user)
        module = content.module
        content.item.delete()
        content.delete()
        return redirect('inner_post_list', module.id)


class PostContentListing(TemplateResponseMixin, View):
    template_name = 'publications/manage/module/content_list.html'

    def get(self, request, module_id):
        module = get_object_or_404(Module, id=module_id, post__publisher=request.user)
        return self.render_to_response({'module': module})


class CategoryListing(TemplateResponseMixin, View):
    model = Post
    template_name = 'publications/posts/listing_posts.html'

    def get(self, request, category=None):
        categories = Category.objects.annotate(total_posts=Count('posts'))
        posts = Post.objects.annotate(total_modules=Count('modules'))

        if category:
            category = get_object_or_404(Category, slug=category)
            posts = posts.filter(category=category)
        return self.render_to_response({'categories': categories, 'category': category, 'posts': posts})


class PostDetailsText(DetailView):
    model = Post
    template_name = 'publications/posts/posts_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['enroll_form'] = PostFollowingForm(initial={'post_follow_field': self.object})
        return context







