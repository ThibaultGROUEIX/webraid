from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^test$', views.test),
    url(r'^new_category$', views.new_category, name='new_category'),
    url(r'^new_album$', views.new_album, name='new_album'),
    url(r'^new_photo$', views.new_photo, name='new_photo'),
    url(r'^view_photo/(?P<id_category>\d+)/(?P<id_album>\d+)/(?P<id_photo>\d+)$', views.view_photo),
    #url(r'^(?P<pk>\d+)/ajax-upload/$' , views.AjaxPhotoUploadView.as_view(),'ajax_photo_upload_view'),

]