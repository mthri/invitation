from django import template

register = template.Library()

@register.filter(name='none_replace')
def none_replace(data, replace_with=''):
    if data:
        return data
    else:
        return replace_with