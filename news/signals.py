from django.db.models.signals import m2m_changed, pre_save, post_save
from django.dispatch import receiver  # импортируем нужный декоратор
from django.core.mail import mail_admins
from .models import Post, Category, PostCategory
from datetime import datetime
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string




@receiver(m2m_changed, sender=Post.category.through)
def subscribers_notification(sender, instance, **kwargs):
    """Оповещение подписчиков на данные категории при создании нового поста.
    При создании поста рассылает письма подписчикам каждой его категории."""
    action = kwargs.pop('action', None)

    if action == 'post_add':
        for category in instance.category.all():
            for sub in category.subs.all():
                html_content = render_to_string(
                    'notification_created.html',
                    {
                        'user': sub.user,
                        'post': instance,
                    }
                )
                msg = EmailMultiAlternatives(
                    subject=f'{sub.user.username.capitalize()}',
                    body=instance.text,  # это то же, что и message
                    from_email='lutsckov.o@yandex.ru',
                    to=[sub.user.email],  # это то же, что и recipients_list
                )
                msg.attach_alternative(html_content, "text/html")  # добавляем html
                msg.send()  # отсылаем

