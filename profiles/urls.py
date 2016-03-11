from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home_redirect),
    url(r'^home/$', views.dashboard,
        name='dashboard'),
    url(r'^users/$', views.UserProfilesListView.as_view(),
        name='profiles-list'),
    url(r'^users/(?P<user_id>\d+)/$', views.view_profile,
        name='profile-detail'),
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout',
        {'next_page': '/logged_out/'}),
<<<<<<< HEAD
    url(r'^logged_out/$', views.view_logged_out),
    url(r'^password_change/$', 'django.contrib.auth.views.password_change', name='password_change'),
    url(r'^password_change/done/$', 'django.contrib.auth.views.password_change_done', name='password_change_done'),
    url(r'^edit_user_profile/$', views.detailed_user_profile_form, name='self_edit_user_profile')
=======
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

    # Profile edition urls
    url(r'^edit_profile/$',
        views.edit,
        name='self_edit_user_profile'),
    url(r'^edit_profile/all/$',
        views.detailed_user_profile_form,
        name='self_edit_user_profile_all'),
    url(r'^edit_profile/names/$',
        views.edit_name,
        name='self_edit_name'),
    url(r'^edit_profile/address/$',
        views.edit_fulladdress,
        name='self_edit_address'),
    url(r'^edit_profile/coordinates/$',
        views.edit_coordinates,
        name='self_edit_coordinates'),
    # Return array of users for tagging
    url(r'^users_json',
        views.gen_users_json,
        name='users_json'
        )
>>>>>>> 9350566dfec21f0cd1aad032f264d82b996d8fba
]
