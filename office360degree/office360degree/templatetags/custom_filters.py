# custom_filters.py
from django import template

register = template.Library()

@register.filter(name='get_category')
def get_category(dictionary, key):
    return dictionary.get(key)
