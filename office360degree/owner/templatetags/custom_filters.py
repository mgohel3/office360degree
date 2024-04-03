from django import template

register = template.Library()

@register.filter(name='filter_role')
def filter_role(users_list, role):
    return [user for user in users_list if getattr(user, f'is_{role}')]

@register.filter(name='get_category')
def get_category(dictionary, key):
    return dictionary.get(key)