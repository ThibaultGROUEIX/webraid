from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^account_creation_example/$', views.account_creation,
        name='render_account_creation_email'),
]
