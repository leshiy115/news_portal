from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Author(models.Model):
    """1. Модель, содержащая объекты всех авторов."""
    # cвязь «один к одному» с встроенной моделью пользователей User;
    ##!! Не проходила миграция. Вместо 'User' прописал в поле User (без кавычек). Может все стоит без кавычек прописывать? ошибка: news.Author.user: (fields.E307) The field news.Author.user was declared with a lazy reference to 'news.user', but app 'news' doesn't provide model 'user'.

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    # рейтинг пользователя.
    rating = models.IntegerField(default=0)



class Category(models.Model):
    """2. Категории новостей/статей — темы, которые они отражают (спорт, политика, образование и т. д.)."""
    name = models.CharField(max_length=20, unique=True)



class Post(models.Model):
    """3. Эта модель должна содержать в себе статьи и новости, которые создают пользователи. Каждый объект может иметь одну или несколько категорий."""
    # поле с выбором — «статья» или «новость»;
    post = 'P'
    news = 'N'
    POSITIONS = [(post, 'Статья'),
                 (news, 'Новости')]
    position = models.CharField(max_length=1, choices=POSITIONS, default=post)
    # автоматически добавляемая дата и время создания;
    time_created = models.DateTimeField(auto_now_add=True)
    # заголовок статьи/новости;
    title = models.CharField(max_length=255, unique=True)
    # текст статьи/новости;
    text = models.TextField()
    # рейтинг статьи/новости.
    rating = models.IntegerField(default=0)
    # связь «один ко многим» с моделью Author;
    #!! Можно было при удалении поста авторство перетекало админу и отображалось бы как "Неизвестный автор" или имя сохранялось в отдельную модель и отражалось бы от туда. Так бы пост мог оставаться на сайте. Но думаю это нарушении авторских прав. Если стоит это провернуть напиши в ответе.
    author = models.ForeignKey('Author', null=True, on_delete=models.CASCADE)
    # связь «многие ко многим» с моделью Category (с дополнительной моделью PostCategory);
    category = models.ManyToManyField('Category', through='PostCategory')



class PostCategory(models.Model):
    """4. Промежуточная модель для связи «многие ко многим»:"""
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)



class Comment(models.Model):
    """5. Под каждой новостью/статьёй можно оставлять комментарии, поэтому необходимо организовать их способ хранения тоже."""
    #todo стоит подумать как создать модели для комментирования комментариев.

    # текст комментария;
    text = models.TextField()
    # дата и время создания комментария;
    time_created = models.DateTimeField(auto_now_add=True)
    # рейтинг комментария.
    rating = models.IntegerField(default=0)
    # связь «один ко многим» с моделью Post;
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    # связь «один ко многим» со встроенной моделью User (комментарии может оставить любой пользователь, необязательно автор);
    user = models.ForeignKey(User, on_delete=models.CASCADE)


