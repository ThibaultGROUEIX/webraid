from django import template

register = template.Library()
# Templatetags useful for displaying a link depending on the current url
# For example, we don't want to display the home link on the home page
# From https://gist.github.com/timmyomahony/2049936


class NavSelectedNode(template.Node):
    def __init__(self, obj, var):
        self.obj = obj
        self.var = var

        def render(self, context):
            value = template.Variable(self.obj).resolve(context)
            context[self.var] = False
            path = context['request'].path
            # Here we can do some more complicated parsing of the current URL against our passed URL
            if (path.startswith(value)) or (value == path):
                context[self.var] = True
                return ""


@register.tag(name='is_active')
def is_active(parser, token):
    """Check if the provided string pattern is the current url"""
    args = token.split_contents()
    template_tag = args[0]
    if len(args) != 4:
        raise template.TemplateSyntaxError, "%r tag should be in the form {%% is_active [obj] as [variable] %%}" % template_tag
    return NavSelectedNode(args[1], args[3])

    # {% url someview as an_url %}
    # {% is_active an_url as is_home_page %}
    # {% if is_home_page %}...{% endif %}
