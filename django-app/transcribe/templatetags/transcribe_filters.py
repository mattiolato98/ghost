import datetime

from django.template.defaulttags import register


@register.filter
def to_datetime(seconds):
    return datetime.datetime.fromtimestamp(seconds)
