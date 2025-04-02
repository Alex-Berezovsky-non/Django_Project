from django import template

register = template.Library()

@register.filter(name='status_color')
def status_color(value):
    colors = {
        'новая': 'warning',
        'подтвержденная': 'primary',
        'отмененная': 'danger',
        'выполненная': 'success',
    }
    return colors.get(value, 'secondary')