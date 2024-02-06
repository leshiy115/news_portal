from datetime import datetime
from pprint import pprint

from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
from .models import Category, Post, Author, PostCategory, Comment


class NewsList(ListView):
    model = Post
    ordering = '-time_created'
    template_name = 'news.html'
    context_object_name = 'posts'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # pprint(context)
        return context


class PostDetail(DetailView):
    model = Post
    template_name = "post.html"
    context_object_name = 'post'



# def about(request):
#     return render(request, 'estimate/about.html', {'title': 'О сайте'})














