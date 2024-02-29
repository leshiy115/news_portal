from django.db.models.signals import m2m_changed
from django.dispatch import receiver  # импортируем нужный декоратор
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .tasks import new_post_notification
from .models import Post


@receiver(m2m_changed, sender=Post.category.through)
def subscribers_notification(sender, instance, **kwargs):
    """Оповещение подписчиков на данные категории при создании нового поста.
    При фиксации создании поста и его связи многие ко многим к категории(ям),
     через создание такси в celery, подписчикам рассылаются письма если они подписаны на данную категорию."""

    action = kwargs.pop('action', None)

    if action == 'post_add':  # если произошло создание нового поста
        print('instance.pk == ', instance.pk)
        # Создаем таску в celery для отправки почты
        new_post_notification.delay(post_id=instance.pk)

