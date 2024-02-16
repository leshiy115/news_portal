from datetime import datetime
from pprint import pprint

from django.utils import timezone
from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic import (ListView, DetailView, CreateView,
                                  UpdateView, DeleteView)
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth.mixins import PermissionRequiredMixin


from .models import Category, Post, Author, PostCategory, Comment
from .filters import PostFilter
from .forms import PostForm



class PostsList(ListView):
    model = Post
    ordering = '-time_created'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10


    def get_queryset(self):
        queryset = super().get_queryset()

        if not self.request.path or self.request.path == '/':
            return queryset

        if 'news/' in self.request.path:
            queryset = queryset.filter(post_type="N")
            print('queryset = N')

        if 'articles/' in self.request.path:
            queryset = queryset.filter(post_type="A")
            print('queryset = A')

        if 'search/' in self.request.path:
            self.filterset = PostFilter(self.request.GET, queryset)
            print('RETURNING WITH SEARCH')
            return self.filterset.qs

        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'search/' in self.request.path:
            context['filterset'] = self.filterset
        return context



class PostDetail(LoginRequiredMixin, DetailView):

    model = Post
    template_name = "post.html"
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pprint(context)
        return context


class UserDetail(LoginRequiredMixin, DetailView):
    """Для отображения профиля"""
    model = User
    template_name = "user_profile.html"
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_premium'] = not self.request.user.groups.filter(name='authors').exists()
        return context


def upgrade_me(request):
    """Изменение уровня доступа через профиль"""
    user = request.user
    premium_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        premium_group.user_set.add(user)
    return redirect(f'/user_profile/{user.pk}')



class PostCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post')
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


    def form_valid(self, form):
        post = form.save(commit=False)
        # проверяем запрос идет из новостей или постов
        path = self.request.path
        if 'news/' in path:
            post.post_type = "N"
        elif 'articles/' in path:
            post.post_type = "A"
        else:
            raise Exception(f'Принятый путь не верен - class PostCreate(CreateView):'
                            f'\nself.request.path == {self.request.path}')

        # проверяем что юзер залогинился
        if self.request.user.pk is None:
            raise Exception('Так как вы не авторизованны, вы не можете создавать посты')
        else:
            post.author = self.request.user.author

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_type'] = self.request.path[1]
        print(self.request.path[1])

        return context



class PostUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post')
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_premium'] = not self.request.user.groups.filter(name='authors').exists()
        return context


# пришлось написать 2 отдельных вьюшки для удаления. так меньше кода.
# Разница лишь в пути реверса. Потом можно удалить и отправлять на общую.
class PostDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post')
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('all_posts')







