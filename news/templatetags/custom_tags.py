from django import template
from datetime import datetime
import pytz

register = template.Library()


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    return d.urlencode()


@register.simple_tag
def clock(tz):
    clock = datetime.now(pytz.timezone(tz)).strftime("%H:%M")
    hour = int(datetime.now(pytz.timezone(tz)).strftime("%H"))
    return {'clock': clock, 'hour': hour}

