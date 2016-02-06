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
