from django import template

register = template.Library()

@register.filter(name='priority_color')
def priority_color(value):
    color_map = {
        'high': 'bg-red-100',
        'medium': 'bg-darkGray',
        'low': 'bg-green-100',
    }
    return color_map.get(value.lower(), 'bg-red-100')