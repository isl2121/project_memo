from django import template

register = template.Library()

@register.filter(is_safe=False)
def modulo(value, arg):
    return int(value) % int(arg)


@register.filter()
def to_int(value):
    return int(value)