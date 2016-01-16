from BeautifulSoup import BeautifulSoup as Bs

from django import template
from django.core.urlresolvers import reverse

from webraid import settings

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


@register.simple_tag(name="css_active_url")
def css_active_url(current_url, urlname):
    if current_url == reverse(urlname):
        return "active"
    else:
        return ""


@register.simple_tag(name='init_fuzzy_search')
def init_fuzzy_search(container_name, attribute_list):
    list = "<script type=\"text/javascript\" src=\"" + settings.STATIC_URL + "js/list.js\"></script>"
    fuzzy_search = "<script type=\"text/javascript\" src=\"" + settings.STATIC_URL + "js/list.fuzzysearch.min.js\"></script>"
    script = "<script>var objects_list = new List('" + container_name + \
             "', { valueNames:[" + attribute_list + "], plugins: [ListFuzzySearch()]});</script>"

    return list + fuzzy_search + script


@register.simple_tag(name='input_fuzzy_search')
def input_fuzzy_search(placeholder=""):
    tag = "<input type=\"search\" class=\"fuzzy-search\" placeholder=\"" + placeholder + "\" autofocus>" \
                                                                                         "<i class =\"fa fa-fw fa-search\"></i>"
    wrapper = Bs("<div class=\"searchbar\"></div>")
    tag = Bs(tag)
    wrapper.div.append(tag)
    return wrapper.__str__()


@register.simple_tag(name='pretty_user_tag')
def pretty_user_tag(user_profile):
    return Bs(
        "<a href=\"" +
        user_profile.get_absolute_url() +
        "\" class =\"tag tag-orange active\">" + user_profile.user.username + "</span>"
    ).__str__()


@register.simple_tag(name='pretty_thread_path')
def pretty_thread_path(thread):
    return Bs(
        "<a href=\"" + thread.category.get_absolute_url() + "\"> "
        + thread.category.name
        + "</a> / "
        + "<a href=\"" + thread.get_absolute_url() + "\">"
        + thread.title
        + "</a>"
    ).__str__()
