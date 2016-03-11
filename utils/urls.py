from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^tags$',
        views.get_tags,
        name="get_tags"
        )
]
