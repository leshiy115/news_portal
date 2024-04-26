from datetime import datetime
from pprint import pprint

import requests
from django.utils import timezone
from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic import (ListView, DetailView, CreateView,
                                  UpdateView, DeleteView, View)
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth.mixins import PermissionRequiredMixin



from .models import Category, Post, Author, PostCategory, Comment
from .filters import PostFilter
from .forms import PostForm, SubscriptionsForm
from .tasks import new_post_notification


class PostsList(ListView):
    model = Post
    ordering = '-time_created'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10


    def get_queryset(self):
        queryset = super().get_queryset()

        if not self.request.path or self.request.path == '/':

            # return queryset1  # тестовая ошибка
            return queryset

        if 'news/' in self.request.path:
            queryset = queryset.filter(post_type="N")

        if 'articles/' in self.request.path:
            queryset = queryset.filter(post_type="A")

        if 'search/' in self.request.path:
            self.filterset = PostFilter(self.request.GET, queryset)
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


# class Subscribe(LoginRequiredMixin, CreateView):


class PostCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'news.add_post'
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


    def form_valid(self, form):
        post = form.save(commit=False)
        path = self.request.path
        if not check_user_limit(self.request.user):
            return redirect('all_posts')


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

        # Проверка на лимит для юзера. Если лимит превышен
        # форма в контексте обнуляется и шаблон выдает сообщение о превышении лимита.
        if check_user_limit(self.request.user):
            context['post_type'] = self.request.path[1]
            return context
        else:
            context['form'] = None
            return context





class PostUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'news.change_post'
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_premium'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class PostDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post')
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('all_posts')


class Subscriptions(LoginRequiredMixin, UpdateView):
    form_class = SubscriptionsForm
    model = Author
    template_name = 'subscriptions.html'


def check_user_limit(user):
    """Проверка юзеров на превышение лимита на создание постов.
    Лимит == 3 в день по UTC"""
    from datetime import datetime
    import pytz
    author = user.author

    # только у первого админа нет лимита на создание постов.
    if user.pk == 1:
        return True

    same_day = 0
    last3 = author.post_set.order_by('-time_created')[:3].values_list('time_created')
    for time_created in last3:
        day = time_created[0].date()
        if day == datetime.now(pytz.utc).date():
            same_day += 1
    if same_day >= 3:
        return False
    else:
        return True


from django.http import HttpResponse
from django.utils.translation import gettext as _  # импортируем функцию для перевода


# Create your views here.

class TransTest(View):
    def get(self, request):
        string = _('Hello world')

        return HttpResponse(string)

