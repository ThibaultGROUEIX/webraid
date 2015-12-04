from django.contrib import admin

# Register your models here.
from gallery import models



# Register the profiles models for administration
admin.site.register(models.Category)
admin.site.register(models.Album)
admin.site.register(models.Picture)
admin.site.register(models.UploadFile)
