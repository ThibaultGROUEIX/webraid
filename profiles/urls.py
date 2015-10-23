from django.conf.urls import url
from . import views
from django.contrib import auth

urlpatterns = [
    url(r'users/', views.UserProfilesListView.as_view(),
        name='profiles-list'),
    url(r'login/', 'django.contrib.auth.views.login'),
    url(r'logout/', 'django.contrib.auth.views.logout'),
]
