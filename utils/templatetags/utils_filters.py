from django import template

register = template.Library()


@register.filter(name='addcss')
def addcss(value, arg):
    return value.as_widget(attrs={'class': arg})


@register.filter(name='form_control')
def form_control(value):
    return value.as_widget(attrs={'class': 'form-control'})


@register.filter(name='wrap_col')
def wrap_col(value, css_size):
    return "<div class=\"" + css_size + "\">" + value + "</div>"
