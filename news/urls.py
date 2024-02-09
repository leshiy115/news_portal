from django.urls import path
# Импортируем созданное нами представление
from .views import (PostsList, PostDetail, PostCreate,
                    PostUpdate, ArticlesDelete, NewsDelete)

#todo После сдачи задания удалить лишнее.
urlpatterns = [
   path('', PostsList.as_view(), name='all_posts'),
   path('news/', PostsList.as_view(), name='news'),
   path('news/search/', PostsList.as_view(), name='news_search'),
   path('articles/', PostsList.as_view(), name='articles'),
   path('articles/search/', PostsList.as_view(), name='articles_search'),

   path('news/<int:pk>/', PostDetail.as_view(), name='news_detail'),
   path('articles/<int:pk>/', PostDetail.as_view(), name='articles_detail'),

   path('news/create/', PostCreate.as_view(), name='news_create'),
   path('articles/create/', PostCreate.as_view(), name='articles_create'),

   path('news/<int:pk>/edit/', PostUpdate.as_view(), name='news_edit'),
   path('articles/<int:pk>/edit/', PostUpdate.as_view(), name='articles_edit'),

   path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
   path('articles/<int:pk>/delete/', ArticlesDelete.as_view(), name='articles_delete'),
]

