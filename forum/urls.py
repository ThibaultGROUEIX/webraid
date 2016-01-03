from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$',
        views.ThreadCategoryListView.as_view(), name='forum'),

    url(r'^add_category/$',
        views.AddThreadCategoryView.as_view(), name='add_thread_category'),

    url(r'^category/(?P<slug>[\w-]+)/$',
        views.thread_category_detail, name='detail_thread_category'),

    url(r'^category/(?P<slug>[\w-]+)/edit/(?P<pk>\d+)/$',
        views.thread_category_detail, name='detail_thread_category_edit_thread'),

    url(r'^category/(?P<category_slug>[\w-]+)/thread/(?P<slug>[\w-]+)/$',
        views.thread_detail, name='detail_thread'),

    url(r'^category/(?P<category_slug>[\w-]+)/thread/(?P<slug>[\w-]+)/edit/(?P<pk>\d+)/$',
        views.thread_detail, name='detail_thread_edit_post'),

    url(r'delete_post/(?P<post_id>\d+)$',
        views.post_delete,
        name='detail_thread_delete_post')
]
