import time

from celery import shared_task

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone

from datetime import timedelta

from .models import Post, Category, PostCategory, Author


@shared_task
def new_post_notification(post_id):
    post = Post.objects.get(pk=post_id)
    for category in post.category.all():
        for sub in category.subs.all():
            html_content = render_to_string(
                'notification_created.html',
                {
                    'user': sub.user,
                    'post': post,
                }
            )
            msg = EmailMultiAlternatives(
                subject=f'{sub.user.username.capitalize()}',
                body=post.text,  # это то же, что и message
                from_email='lutsckov.o@yandex.ru',
                to=[sub.user.email],  # это то же, что и recipients_list
            )
            msg.attach_alternative(html_content, "text/html")  # добавляем html
            print(f"Письмо отправляется юзеру {user.email}\nmsg == {msg}")
            msg.send(fail_silently=True)


@shared_task
def week_notification():
    """Создает рассылку писем юзерам подписавшимся на данную категорию.
    Потестить толком не смогу, рассылка остановилась из-за обвинения в спаме.
    -- https://yandex.ru/support/mail/web/spam.html#troubleshooting__sending-limits"""
    today = timezone.now()
    week_before = today - timedelta(days=7)
    week_posts = Post.objects.filter(time_created__range=(week_before, today))

    for author in Author.objects.all():
        author_cats = author.subscriptions.all()
        if author_cats:  # если юзер подписан на что-то
            posts = week_posts.filter(category__in=author_cats)
            user = author.user

            html_content = render_to_string(
                'week_notification.html',
                {
                    'user': user,
                    'posts': posts,
                }
            )
            msg = EmailMultiAlternatives(
                subject=f'Еженедельная рассылка новостей от News Portal',
                from_email='lutsckov.o@yandex.ru',
                to=[user.email],  # это то же, что и recipients_list
            )
            msg.attach_alternative(html_content, "text/html")  # добавляем html
            print(f"Письмо отправляется юзеру {user.email}\nmsg == {msg}")
            msg.send(fail_silently=True)
