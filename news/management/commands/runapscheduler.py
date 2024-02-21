
import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from news.models import Post, Category, Author
from django.contrib.auth.models import User

from datetime import timedelta
from django.utils import timezone


logger = logging.getLogger(__name__)


def week_notification():
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
            msg.send()  # отсылаем
            print(f'Рассылка из week_notification осуществлена.Дата:{today.date()}')




# функция, которая будет удалять неактуальные задачи
@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """
    This job deletes APScheduler job execution entries older than `max_age` from the database.
    It helps to prevent the database from filling up with old historical records that are no
    longer useful.

    :param max_age: The maximum length of time to retain historical job execution records.
                    Defaults to 7 days.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            week_notification,
            #trigger=CronTrigger(minute="*/1"),  # для теста
            trigger=CronTrigger(week="*/1"),  # То же, что и интервал, но задача тригера таким образом более понятна django
            id="week_notification",  # The `id` assigned to each job MUST be unique.
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'week_notification'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
