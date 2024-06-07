from django import template

register = template.Library()

@register.filter(name = 'get_range')
def get_range(value, arg=None):
    return range(int(value)) if arg is None else range(int(value), int(arg))
