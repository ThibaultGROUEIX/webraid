from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.ThreadCategoryListView.as_view(), name='forum'),
    url(r'^add_category/$', views.AddThreadCategoryView.as_view(), name='add_thread_category'),
    url(r'^category/(?P<slug>[\w-]+)/$', views.thread_category_detail, name='detail_thread_category'),
    url(r'^add_thread/$', views.AddThreadView.as_view(), name='add_thread'),
    url(r'^thread/(?P<slug>[\w-]+)/$', views.thread_detail, name='detail_thread'),
]
