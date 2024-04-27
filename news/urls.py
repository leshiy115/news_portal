from django.urls import path
from .views import (PostsList, PostDetail, PostCreate,
                    PostUpdate, PostDelete,
                    UserDetail, upgrade_me, Subscriptions, TimeZoneChange)
from django.views.decorators.cache import cache_page


#todo После сдачи задания удалить лишнее.
urlpatterns = [
   # path('', cache_page(10)(PostsList.as_view()), name='all_posts'),
   path('', PostsList.as_view(), name='all_posts'),
   path('news/', PostsList.as_view(), name='news'),
   path('news/search/', PostsList.as_view(), name='news_search'),
   path('articles/', PostsList.as_view(), name='articles'),
   path('articles/search/', PostsList.as_view(), name='articles_search'),

   #todo заменить на post/int
   path('news/<int:pk>/', cache_page(60*5)(PostDetail.as_view()), name='news_detail'),
   path('articles/<int:pk>/', PostDetail.as_view(), name='articles_detail'),

   path('news/create/', PostCreate.as_view(), name='news_create'),
   path('articles/create/', PostCreate.as_view(), name='articles_create'),

   path('news/<int:pk>/edit/', PostUpdate.as_view(), name='news_edit'),
   path('articles/<int:pk>/edit/', PostUpdate.as_view(), name='articles_edit'),

   path('news/<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),

   path('user_profile/<int:pk>/', UserDetail.as_view(), name='user_profile'),
   path('upgrade/', upgrade_me, name='upgrade'),
   path('user_profile/<int:pk>/subscriptions/', Subscriptions.as_view(), name='subscriptions'),
   path('time_zone/', TimeZoneChange.as_view(), name='time_zone'),
]

