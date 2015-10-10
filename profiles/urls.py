from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'', views.UserProfilesListView.as_view(),
        name='profiles-list'),
]
