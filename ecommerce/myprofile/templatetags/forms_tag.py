from django import template
from django.forms.boundfield import BoundField

register = template.Library()

@register.filter(name='add_class')
def add_class(value, css_class):
    """
    Adds a CSS class to a form field
    """
    if isinstance(value, BoundField):
        existing_classes = value.field.widget.attrs.get('class', '')
        new_classes = f"{existing_classes} {css_class}".strip()
        return value.as_widget(attrs={'class': new_classes})
    return value

@register.filter(name='add_error_class')
def add_error_class(value, css_class):
    """
    Adds an error class to a form field if it has errors
    """
    if isinstance(value, BoundField) and value.errors:
        existing_classes = value.field.widget.attrs.get('class', '')
        new_classes = f"{existing_classes} {css_class}".strip()
        return value.as_widget(attrs={'class': new_classes})
    return value