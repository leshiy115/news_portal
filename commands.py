import random
from news.models import *

"""Файл всех команд, запускаемых в Django shell.
Сделал немного по своему, так как мне еще понадобятся эти команды для наполнения бд."""

# 1. Создать двух пользователей (с помощью метода User.objects.create_user('username')).
for i in range(1, 4):
    User.objects.create_user(username=f'User{i}', email=f'{i}@mail.ru', password='admin')


# 2. Создать два объекта модели Author, связанные с пользователями.
for user in User.objects.all():  # Админ тоже будет графоманом).
    Author.objects.create(user=user, rating=random.randint(20, 80))


# 3. Добавить 4 категории в модель Category.
cats = ['Юмор', 'Наука', 'Кино', 'Медицина']
for cat in cats:
    Category.objects.create(name=cat)


# 4. Добавить 2(много) статей и 1 (много) новостей.
p_types = ['P', 'N']
for user in User.objects.all():
    for i in range(random.randint(2, 7)):
        Post.objects.create(title=f"Post №{i}. Author: {user.username}",
                            text=f"User={user.username} for post №{i} text №{i}",
                            author=user.author,
                            post_type=random.choices(p_types)[0],  # если не указать индекс 0 вернет list
                            rating=random.randint(0, 30))


# 5 Создание связей между Post и Category
posts = Post.objects.all()
cats = Category.objects.all()
for post in posts:
    PostCategory.objects.create(category=random.choices(cats)[0], post=post)

# добавление еще одной случайной категории к случайному посту
posts = Post.objects.all()
rand_posts = [random.choices(posts)[0] for _ in range(6)]
for post in rand_posts:  # для 3-х случайных постов выбрать еще одну случайною категорию
    p_category = post.category.get()  # находим категорию, которая есть
    cats = list(Category.objects.all())
    cats.remove(p_category)  # удаляем из списка всех категорий уже имеющиеся у поста.
    PostCategory.objects.create(category=random.choices(cats)[0], post=post)


# 6. Создать как минимум 4 комментария к разным объектам модели Post
# (в каждом объекте должен быть как минимум один комментарий).

posts = Post.objects.all()
for user in User.objects.all():
    # каждый юзер оставляет случайное количество комментов на случайном посте
    for i in range(random.randint(4, 10)):
        post = random.choices(posts)[0]
        text = f"{user.username}: comment text №{i} to Post:{post.title}"
        Comment.objects.create(text=text, user=user, post=post, rating=random.randint(0, 10))


# 7. Применяя функции like() и dislike() к статьям/новостям и комментариям, скорректировать рейтинги этих объектов.
for _ in range(20):
    post = random.choices(Post.objects.all())[0]
    if random.randint(0, 1):
        post.like()
    else:
        post.dislike()
    comment = random.choices(Comment.objects.all())[0]
    if random.randint(0, 1):
        comment.like()
    else:
        comment.dislike()


# 8. Обновить рейтинги пользователей.
for author in Author.objects.all():
    print(author)
    print('old rating', author.rating)
    author.update_rating()
    print('new rating', author.rating)


# 9. Вывести username и рейтинг лучшего пользователя (применяя сортировку и возвращая поля первого объекта).
best_author = Author.objects.order_by('-rating').values('user__username', 'rating').first()
print(best_author)

# 10. Вывести дату добавления, username автора, рейтинг, заголовок и превью лучшей статьи,
# основываясь на лайках/дислайках к этой статье.
best_post = Post.objects.order_by('-rating').values('time_created', 'author__user__username', 'rating', 'title', 'pk').first()
post = Post.objects.get(pk=best_post['pk'])
date = best_post['time_created'].strftime("%A, %d. %B %Y %I:%M%p")
user = best_post['author__user__username']
rating = best_post['rating']
title = best_post['title']
text = f"Best post was added {date} by {user}. Rating is {rating}." \
       f"\n{title}\n{post.preview()}"

# 11. Вывести все комментарии (дата, пользователь, рейтинг, текст) к этой статье.
all_comments = Comment.objects.filter(post=post).values('time_created', 'user__username', 'rating', 'text')
for comment in all_comments:
    text = comment['text']
    rating = comment['rating']
    username = comment['user__username']
    date = comment['time_created']
    print(f"{username}:\n   {text}\nRating={rating}. {date.strftime('%A, %d. %B %Y %I:%M%p')}")
