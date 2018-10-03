from django import template

register = template.Library()

@register.filter(name='truncate_lan_code')
def truncate_language_code(text):
    t = text.split('/')
    url = '/'.join(t[2:])
    return url
