from django.db import models
from django.core.urlresolvers import reverse

from utils.snippets.slugifiers import unique_slugify
from profiles.models import UserProfile
from utils.models import Tag


# Create your models here.

class ThreadCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True)
    tags = models.ManyToManyField(Tag)
    slug = models.SlugField(max_length=50,
                            unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('forum.views.thread_category_detail', args=[self.slug])

    def save(self, **kwargs):
        unique_slugify(self, self.name)
        super(ThreadCategory, self).save(**kwargs)


class Thread(models.Model):
    category = models.ForeignKey(ThreadCategory)
    title = models.CharField(max_length=255)
    tags = models.ManyToManyField(Tag)
    slug = models.SlugField(max_length=50,
                            unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        slug_category = self.category.slug
        return reverse('forum.views.thread_detail', args=[slug_category,self.slug])

    def save(self, **kwargs):
        unique_slugify(self, self.title)
        super(Thread, self).save(**kwargs)


class Post(models.Model):
    thread = models.ForeignKey(Thread)
    # Contenu
    text_content = models.TextField()
    author = models.ForeignKey(UserProfile)
    posted_date = models.DateTimeField(auto_now_add=True)
    last_edit_date = models.DateTimeField(auto_now=True)
    # File uploads
    file = models.FileField()
