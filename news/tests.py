from datetime import datetime, timedelta
import pytz
from django.utils import timezone

today = timezone.now()
week_before = today - timedelta(days=7)
posts = Post.objects.filter(time_created__range=(week_before, today))


