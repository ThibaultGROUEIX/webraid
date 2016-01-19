import json

from django.http import HttpResponse

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
