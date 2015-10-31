from django.db import models

from profiles.models import UserProfile

from utils.models import Tag


# Create your models here.

class ThreadCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name


class Thread(models.Model):
    category = models.ForeignKey(ThreadCategory)
    title = models.CharField(max_length=255)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title


class Post(models.Model):
    thread = models.ForeignKey(Thread)
    # Contenu
    text_content = models.TextField()
    author = models.ForeignKey(UserProfile)
    posted_date = models.DateTimeField()
    last_edit_date = models.DateTimeField()
    # File uploads
    file = models.FileField()

