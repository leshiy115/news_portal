from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Author(models.Model):
    """1. Модель, содержащая объекты всех авторов."""
    # cвязь «один к одному» с встроенной моделью пользователей User;
    ##!! Не проходила миграция. Вместо 'User' прописал в поле User (без кавычек). Может все стоит без кавычек прописывать? ошибка: news.Author.user: (fields.E307) The field news.Author.user was declared with a lazy reference to 'news.user', but app 'news' doesn't provide model 'user'.

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    # рейтинг пользователя.
    rating = models.IntegerField(default=0)
    subscriptions = models.ManyToManyField('Category', through='Subscribers',
        verbose_name=_('Categories in a subscription'))

    def __str__(self):
        return self.user.username


    def update_rating(self) -> None:
        """Метод обновляет рейтинг текущего автора"""

        # суммарный рейтинг каждой статьи автора умножается на 3;
        post_ratings = 0
        # суммарный рейтинг всех комментариев к статьям автора.
        post_comments = 0
        for post in self.post_set.all():
            post_ratings += post.rating
            for comment in post.comment_set.all():
                post_comments += comment.rating

        # суммарный рейтинг всех комментариев автора;
        comments_rating = 0
        for comment in Comment.objects.filter(user=self.user):
            comments_rating += comment.rating

        self.rating = post_ratings * 3 + comments_rating + post_comments
        self.save()

    def get_absolute_url(self):
        return reverse('user_profile', args=[str(self.user.id)])


class Category(models.Model):
    """2. Категории новостей/статей — темы, которые они отражают
    (спорт, политика, образование и т. д.)."""
    name = models.CharField(max_length=20, unique=True)
    subs = models.ManyToManyField('Author', through="Subscribers")


    def __str__(self):
        return f"{self.name.capitalize()}"


class Subscribers(models.Model):
    """Модель для подписки на категорию"""

    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)




class Post(models.Model):
    """3. Эта модель должна содержать в себе статьи и новости, которые создают пользователи.
    Каждый объект может иметь одну или несколько категорий."""
    # поле с выбором — «статья» или «новость»;
    article = 'A'
    news = 'N'
    POSITIONS = [(article, _('Article')),
                 (news, _('News'))]
    post_type = models.CharField(max_length=1, choices=POSITIONS, default=article, verbose_name=_('Type'))
    # автоматически добавляемая дата и время создания;
    time_created = models.DateTimeField(auto_now_add=True, verbose_name=_('Publication date'))
    # заголовок статьи/новости;
    title = models.CharField(max_length=255, unique=True, verbose_name=_('Name'))
    # текст статьи/новости;
    text = models.TextField(verbose_name=_("Text"))
    # рейтинг статьи/новости.
    rating = models.IntegerField(default=0, verbose_name=_('Rating'))
    # связь «один ко многим» с моделью Author;
    #!! Можно было при удалении поста авторство перетекало админу и отображалось бы как "Неизвестный автор" или имя сохранялось в отдельную модель и отражалось бы от туда. Так бы пост мог оставаться на сайте. Но думаю это нарушении авторских прав. Если стоит это провернуть напиши в ответе.
    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    # связь «многие ко многим» с моделью Category (с дополнительной моделью PostCategory);
    category = models.ManyToManyField('Category', through='PostCategory', verbose_name=_('Categories'))



    def like(self) -> None:
        self.rating += 1
        self.save()

    def dislike(self) -> None:
        self.rating -= 1
        self.save()

    def preview(self) -> str:
        text = self.text[:20]
        if len(text) == 20:
            text += '...'
        return text

    def add_category(self, category_name: str = None) -> None:
        """Если пост не подходит ни к одной категории можно создать свою
        и связь данный пост с ней"""
        if not category_name:
            if not self.category.all():
                category = Category.objects.get(name="Uncategorized")
                PostCategory.objects.create(category=category, post=self)
        else:
            if self.category.get(name="Uncategorized"):
                del_cat = Category.objects.get(name="Uncategorized")
                PostCategory.objects.filter(category=del_cat, post=self).delete()
            category = Category.objects.get(name=category_name)
            PostCategory.objects.create(category=category, post=self)


    def get_absolute_url(self):
        if self.post_type == "A":
            return reverse('articles_detail', args=[str(self.id)])

        if self.post_type == "N":
            return reverse('news_detail', args=[str(self.id)])


    def __str__(self):
        return self.title



class PostCategory(models.Model):
    """4. Промежуточная модель для связи «многие ко многим»:"""
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)



class Comment(models.Model):
    """5. Под каждой новостью/статьёй можно оставлять комментарии, поэтому необходимо организовать их способ хранения тоже."""
    #todo стоит подумать как создать модели для комментирования комментариев.

    # текст комментария;
    text = models.TextField(verbose_name=_('Text'))
    # дата и время создания комментария;
    time_created = models.DateTimeField(auto_now_add=True, verbose_name=_('Date of creation'))
    # рейтинг комментария.
    rating = models.IntegerField(default=0, verbose_name=_('Rating'))
    # связь «один ко многим» с моделью Post;
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    # связь «один ко многим» со встроенной моделью User (комментарии может оставить любой пользователь, необязательно автор);
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self) -> None:
        self.rating += 1
        self.save()

    def dislike(self) -> None:
        self.rating -= 1
        self.save()





# from news.models import *

# celery -A news_portal control shutdown
# celery -A news_portal worker -l INFO --pool=gevent --concurrency=8
# celery -A news_portal beat -l INFO



