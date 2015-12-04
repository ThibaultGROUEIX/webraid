# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from utils.snippets.slugifiers import unique_slugify

import os

from django.db import models

class UploadFile(models.Model):
	file = models.ImageField(upload_to='gallery/%Y/%m/%d')


class Category(models.Model):
    titre = models.CharField(max_length=100)
    caption = models.TextField(null=True)
    date = models.DateTimeField(auto_now_add=True, auto_now=False,
                                verbose_name="Date d'ajout")
    createur = models.ForeignKey(User, related_name='creator_category')
    contributeurs = models.ManyToManyField(User, related_name='contributor_category')
    slug = models.SlugField(max_length=50,
                            unique=True)
    def save(self, **kwargs):
        unique_slugify(self, self.titre)
        super(Category, self).save(**kwargs)
    def __str__(self):
        """
        Cette methode que nous definirons dans tous les modeles
        nous permettra de reconnaitre facilement les differents objets que
        nous traiterons plus tard et dans l'administration
        """
        return self.slug

class Album(models.Model):
    titre = models.CharField(max_length=100)
    caption = models.TextField(null=True)
    date = models.DateTimeField(auto_now_add=True, auto_now=False,
                                verbose_name="Date d'ajout")
    category = models.ForeignKey(Category)
    createur = models.ForeignKey(User, related_name='creator_album')
    contributeurs = models.ManyToManyField(User, related_name='contributor_album')
    slug = models.SlugField(max_length=50,
                            unique=True)
    def save(self, **kwargs):
        unique_slugify(self, self.titre)
        super(Album, self).save(**kwargs)

    def __str__(self):
        """
        Cette methode que nous definirons dans tous les modeles
        nous permettra de reconnaitre facilement les differents objets que
        nous traiterons plus tard et dans l'administration
        """
        return self.slug


def get_image_path(instance, filename):
    return os.path.join( 'gallery/',str(instance.album.category.slug), str(instance.album.slug), filename)
#'gallery/', '/',

class Picture(models.Model):
    titre = models.CharField(max_length=100)
    image = models.ImageField(upload_to=get_image_path)
    caption = models.TextField(null=True)
    date = models.DateTimeField(auto_now_add=True, auto_now=False,
                                verbose_name="Date d'ajout")
    album = models.ForeignKey(Album)
    createur = models.ForeignKey(User, related_name='creator_picture')
    personnages = models.ManyToManyField(User, related_name='characters')
    slug = models.SlugField(max_length=50,
                            unique=True)
    def __str__(self):
        """
        Cette methode que nous definirons dans tous les modeles
        nous permettra de reconnaitre facilement les differents objets que
        nous traiterons plus tard et dans l'administration
        """
        return self.slug

    def save(self, **kwargs):
        unique_slugify(self, self.titre)
        super(Picture, self).save(**kwargs)