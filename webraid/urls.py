"""webraid URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static

import settings
import profiles.urls
import forum.urls
<<<<<<< HEAD

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^forum/', include(forum.urls)),
    url(r'^', include(profiles.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_URL)
=======
import notifications.urls
import utils.urls

urlpatterns = [
                  url(r'^admin/', include(admin.site.urls)),
                  url(r'^forum/', include(forum.urls)),
                  url(r'^notifications/', include(notifications.urls)),
                  url(r'^u/', include(utils.urls)),
                  url(r'^', include(profiles.urls)),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_URL)
>>>>>>> 9350566dfec21f0cd1aad032f264d82b996d8fba
