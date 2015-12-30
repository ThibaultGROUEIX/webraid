from django.contrib import admin

import models

admin.site.register(models.NoticeType)
admin.site.register(models.NoticeUserPreferences)
admin.site.register(models.ThreadNoticePreference)
admin.site.register(models.CategoryNoticePreference)