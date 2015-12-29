from django.contrib import admin

from .models import EnqueuedAppNotice, EnqueuedEmailNotice

# Register your models here.
admin.site.register(EnqueuedAppNotice)
admin.site.register(EnqueuedEmailNotice)
