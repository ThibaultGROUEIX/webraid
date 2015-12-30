from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$',
        views.ThreadCategoryListView.as_view(), name='forum'),

    url(r'^add_category/$',
        views.AddThreadCategoryView.as_view(), name='add_thread_category'),

    url(r'^(?P<slug>[\w-]+)/$',
        views.thread_category_detail, name='detail_thread_category'),

    url(r'^/(?P<slug>[\w-]+)/(?P<pk>\d+)/edit$',
        views.thread_category_detail, name='detail_thread_category_edit_thread'),

    url(r'^(?P<category_slug>[\w-]+)/(?P<slug>[\w-]+)/$',
        views.thread_detail, name='detail_thread'),

    url(r'^(?P<category_slug>[\w-]+)/(?P<slug>[\w-]+)/(?P<pk>\d+)/edit$',
        views.thread_detail, name='detail_thread_edit_post'),
]
