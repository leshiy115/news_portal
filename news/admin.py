from django.contrib import admin
from news.models import Author, Post, PostCategory, Category, Comment, Subscribers


# Register your models here.
admin.site.register([Author, Post, PostCategory, Category, Comment, Subscribers])
