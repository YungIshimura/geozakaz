from django import template

register = template.Library()

@register.simple_tag
def verbose_name_tag(obj, field_name):
    return obj._meta.get_field(field_name).verbose_name


@register.filter(name='split')
def split(value, key):
    """
        Returns the value turned into a list.
    """
    return value.split(key)