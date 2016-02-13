from BeautifulSoup import BeautifulSoup as Bs

from django import template
from django.template.loader import render_to_string

register = template.Library()


@register.simple_tag(name="pretty_tag")
def pretty_tag(tag):
    return "<a class=\"tag\" href=\"" + tag.get_absolute_url() + "\">" + tag.tag + "</a>"


@register.simple_tag(name="pretty_post")
def pretty_post(post):
    return render_to_string('utils/pretty/post.html',
                            {"post": post})


@register.simple_tag(name="pretty_short_post")
def pretty_short_post(post):
    return render_to_string('utils/pretty/short_post.html',
                            {"post": post})


@register.simple_tag(name="pretty_thread")
def pretty_thread(thread):
    return render_to_string('utils/pretty/thread.html',
                            {"thread": thread,
                             "last_posts": thread.get_last_posts(limit=5)})


# Prettifiers

@register.simple_tag(name='pretty_user_tag')
def pretty_user_tag(user_profile, additional_info=None):
    if additional_info is not None:
        add = " <b class=\"info\">" + str(additional_info) + "</b>"
    else:
        add = ""
    return Bs(
            "<a href=\"" +
            user_profile.get_absolute_url() +
            "\" class =\"tag tag-orange active\">" + user_profile.user.username + add + "</span>"
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
