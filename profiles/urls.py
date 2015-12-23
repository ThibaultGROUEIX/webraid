from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$',
        views.home_redirect),
    url(r'^home/$',
        views.dashboard,
        name='dashboard'),
    url(r'^users/$',
        views.UserProfilesListView.as_view(),
        name='profiles-list'),
    url(r'^users/(?P<user_id>\d+)/$',
        views.view_profile,
        name='profile-detail'),
    url(r'^login/$',
        'django.contrib.auth.views.login',
        {'template_name': 'forms/login.html'},
        name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout',
        {'next_page': '/logged_out/'}),
    url(r'^logged_out/$',
        views.view_logged_out),
    url(r'^password/$',
        'django.contrib.auth.views.password_change',
        {'template_name': 'forms/password_change.html'},
        name='password_change'),
    url(r'^password_change/done/$',
        'django.contrib.auth.views.password_change_done',
        {'template_name': 'forms/password_change_done.html'},
        name='password_change_done'),
    url(r'^edit_user_profile/$', views.detailed_user_profile_form, name='self_edit_user_profile')
]
