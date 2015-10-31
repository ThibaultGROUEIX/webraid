from django.contrib import admin
from profiles import models


# Register the profiles models for administration
admin.site.register(models.UserProfile)
admin.site.register(models.Address)
admin.site.register(models.School)
admin.site.register(models.StudiesDomain)
admin.site.register(models.City)
admin.site.register(models.CallingCode)