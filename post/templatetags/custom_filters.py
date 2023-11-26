from django import template
from django.utils.timesince import timesince
from datetime import datetime, timedelta
from django.utils import timezone


register = template.Library()

@register.filter(name='custom_timesince')
def custom_timesince(value):
    # now = datetime.now()
    now = timezone.now()
    delta = now - value

    # If the time difference is less than a day, use timesince
    if delta < timedelta(days=1):
        return timesince(value) + ' ago'
    else:
        # If more than a day, format as date and time
        return value.strftime('%b %d, %Y %I:%M %p')
