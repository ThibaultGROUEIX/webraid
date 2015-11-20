from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^test$', views.test),
    url(r'^new_category$', views.new_category),
    url(r'^new_album$', views.new_album),
    url(r'^new_photo$', views.new_photo),


]
