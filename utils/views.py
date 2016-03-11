import json

from django.http import HttpResponse
from django.shortcuts import render

from forum.models import PostTag, Thread
from models import Tag


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
            related_posts = PostTag.objects.filter(tag=tag)
            related_threads = Thread.objects.filter(tags__tag__startswith=tag.tag)
            # Get some nice stats out of the posts / thread, such as the dates
            use_dates = [post_tag.post.posted_date for post_tag in related_posts]
            use_dates.extend([thread.creation_date for thread in related_threads])
            # Aggregate the dates by month-year
            monthly_use = {}
            for date in use_dates:
                key = (date.year, date.month)
                if key in monthly_use:
                    monthly_use[key] += 1
                else:
                    monthly_use[key] = 1

            tag_list.append({
                "tag": tag,
                "related_posts": related_posts,
                "related_threads": related_threads,
                "monthly_use": monthly_use
            })
        except Tag.DoesNotExist:
            pass

    return render(request,
                  'utils/showtags.html',
                  {'tag_summaries': tag_list})
