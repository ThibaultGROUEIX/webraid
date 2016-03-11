from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^tags$',
        views.get_tags,
        name="get_tags"
        ),
    url(r'^tag/(?P<tags>\w+)$',
        views.show_tag,
        name="show_tag")
]
