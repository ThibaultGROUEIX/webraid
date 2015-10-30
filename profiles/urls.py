from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'users/', views.UserProfilesListView.as_view(),
        name='profiles-list'),
    url(r'login/', 'django.contrib.auth.views.login'),
    url(r'logout/', 'django.contrib.auth.views.logout',
        {'next_page': '/logged_out/'}),
    url(r'logged_out', views.view_logged_out),
    url(r'password_change/', 'django.contrib.auth.views.password_change', name='password_change'),
    url(r'password_change/done/', 'django.contrib.auth.views.password_change_done', name='password_change_done'),
    url(r'edit_user_profile/', views.detailed_user_profile_form, name='self_edit_user_profile')
]
