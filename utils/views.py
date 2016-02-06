import json

from django.http import HttpResponse
from django.shortcuts import render

from models import Tag
from forum.models import PostTag, Thread


def get_tags(request):
    if request.GET:
        term = request.GET['term']
    else:
        term = ''
    r = []
    for tag in Tag.objects.filter(tag__contains=term):
        r.append({'value': tag.pk, 'label': tag.tag})

    return HttpResponse(json.dumps(r), content_type="application/json")


def show_tag(request, tags):
    tag_list = []
    for tag_word in tags.split('+'):
        try:
            tag = Tag.objects.get(tag=tag_word)
            related_posts = PostTag.objects.filter(tag=tag)[:10]
            related_threads = Thread.objects.filter(tags__tag__startswith=tag.tag)[:10]
            tag_list.append({
                "tag": tag,
                "related_posts": related_posts,
                "related_threads": related_threads
            })
        except Tag.DoesNotExist:
            pass

    return render(request,
                  'utils/showtags.html',
                  {'tag_summaries': tag_list})
