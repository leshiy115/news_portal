from django.contrib import admin
from news.models import Author, Post, PostCategory, Category, Comment, Subscribers
from modeltranslation.admin import TranslationAdmin

class CategoryAdmin(TranslationAdmin):
    model = Category

class PostAdmin(TranslationAdmin):
    model = Post




# Register your models here.
admin.site.register([Author, Post, PostCategory, Category, Comment, Subscribers])
