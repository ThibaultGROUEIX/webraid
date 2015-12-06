from BeautifulSoup import BeautifulSoup as Bs

from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from django import template

register = template.Library()


class BootstrapificationError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


@register.filter(name='fa_return', is_safe=True)
def prefix_fa_return_arrow(value):
    text = conditional_escape(value)
    return mark_safe("<i class=\"fa fa-arrow-left\"></i> " + text)


@register.filter(name='fa_goto', is_safe=True)
def prefix_fa_return_arrow(value):
    text = conditional_escape(value)
    return mark_safe("<i class=\"fa fa-arrow-right\"></i> " + text)


@register.filter(name='bs_form_input', is_safe=True)
def bootstrapify_form_input(value, label):
    html_str = str(value)
    body = Bs(html_str)

    if body.input is not None:
        input_tag = body.input
    elif body.select is not None:
        input_tag = body.select
    elif body.textarea is not None:
        input_tag = body.textarea
    else:
        raise BootstrapificationError("This is not a form input in bs_form_input")

    if input_tag.has_key('value'):
        input_tag['value'] = conditional_escape(input_tag['value'])

    if input_tag.has_key('class'):
        input_tag['class'] = ' '.join([input_tag['class'], 'form-control'])
    else:
        input_tag['class'] = 'form-control'

    wrapper = Bs("<div class=\"form-group\"></div>")
    lab = Bs("<label>" + label + "</label>")
    lab.label['class'] = 'control-label'
    lab.label['for'] = conditional_escape(input_tag['id'])
    wrapper.div.append(lab)
    wrapper.div.append(input_tag)

    return mark_safe(wrapper.__str__())


@register.filter(name='bs_form_input_h', is_safe=True)
def bootstrapify_h_form_input(value, label):
    html_str = bootstrapify_form_input(value, label)
    body = Bs(html_str)
    body.div.label['class'] = " ".join([body.div.label['class'], 'col-sm-4'])
    div_wrapping = Bs("<div class=\"col-sm-8\"></div>")
    if body.div.input is not None:
        input_tag = body.div.input.extract()
    elif body.div.select is not None:
        input_tag = body.div.select.extract()
        input_tag['class'] = "selectpicker"
        input_tag['data-live-search'] = "true"
    elif body.div.textarea is not None:
        input_tag = body.div.textarea.extract()
    else:
        raise BootstrapificationError("Not a correct form group in bs_form_input_h")

    div_wrapping.div.append(input_tag)
    body.div.insert(1, div_wrapping)

    return mark_safe(body.__str__())


@register.filter(name='bs_2col', is_safe=True)
def boostrapify_wrap_in_half_column(value):
    html_str = str(value)
    body = Bs(html_str)
    div_wrapping = Bs("<div class=\"col-lg-6 col-md-6 col-sm-12\"></div>")
    div_wrapping.div.append(body)

    return mark_safe(div_wrapping.__str__())
