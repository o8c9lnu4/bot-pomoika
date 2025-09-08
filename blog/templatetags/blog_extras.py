from django import template
from django.utils.html import linebreaks

register = template.Library()

@register.filter
def linebreaks_filter(text):
    return linebreaks(text) 