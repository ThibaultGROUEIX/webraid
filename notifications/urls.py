from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'follow-thread/(?P<thread_slug>[\w-]+)',
        views.follow_thread,
        name='follow_thread'),
    url(r'follow-category/(?P<category_slug>[\w-]+)',
        views.follow_category,
        name='follow_category'),
    url(r'^account_creation_example/$', views.account_creation,
        name='render_account_creation_email'),
]
