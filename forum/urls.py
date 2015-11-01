from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.ThreadCategoryListView.as_view(), name='forum')
]
