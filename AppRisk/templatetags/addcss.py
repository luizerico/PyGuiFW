from django import template
register = template.Library()

@register.filter(name='addcss')
def addcss(value, arg):
    attrs = value.field.widget.attrs
    orig = attrs['class'] if 'class' in attrs else ''

    attrs['class'] = arg + ' ' + orig

    rendered = str(value)

    return rendered