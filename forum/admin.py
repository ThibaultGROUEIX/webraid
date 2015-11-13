from django.contrib import admin

from forum import models
# Register your models here.
admin.site.register(models.ThreadCategory)
admin.site.register(models.Thread)