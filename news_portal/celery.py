import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_portal.settings')

app = Celery('news_portal')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'week_notification_monday_8am': {
        'task': 'news.tasks.week_notification',
        # 'schedule': crontab(minute='*/3'),  # для теста
        'schedule': crontab(minute=0, hour=8, day_of_week='monday'),
    },
}

