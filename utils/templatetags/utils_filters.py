from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name='addcss')
def addcss(value, arg):
    return value.as_widget(attrs={'class': arg})


@register.filter(name='displaytags', is_safe=True)
def displaytags(value):
    s = []
    for tag in value:
        s.append("<span class=\"tag\">" + conditional_escape(tag.__str__()) + "</span>")

    taglist = " ".join(s)
    return mark_safe(taglist)


@register.filter(name='form_control')
def form_control(value):
    return value.as_widget(attrs={'class': 'form-control'})


@register.filter(name='truncatemod')
def truncatemod(value, max_length=140):
    if len(value) > max_length:
        truncd_val = value[:max_length]
        if not len(value) == max_length + 1 and value[max_length + 1] != " ":
            truncd_val = truncd_val[:truncd_val.rfind(" ")]
        return truncd_val + "..."
    return value


@register.filter(name='wrap_col')
def wrap_col(value, css_size):
    return "<div class=\"" + css_size + "\">" + value + "</div>"


@register.filter(name='info_text_sm', is_safe=True)
def info_text_sm(value):
    return mark_safe("<span class=\"info-text-sm\">" + conditional_escape(value) + "</span>")
