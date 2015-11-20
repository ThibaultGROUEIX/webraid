# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    titre = models.CharField(max_length=100)
    caption = models.TextField(null=True)
    date = models.DateTimeField(auto_now_add=True, auto_now=False,
                                verbose_name="Date d'ajout")
    createur = models.ForeignKey('User')
    contributeurs = models.ManyToManyField('User')


    def __str__(self):
        """
        Cette methode que nous definirons dans tous les modeles
        nous permettra de reconnaitre facilement les differents objets que
        nous traiterons plus tard et dans l'administration
        """
        return self.titre


class Album(models.Model):
    titre = models.CharField(max_length=100)
    caption = models.TextField(null=True)
    date = models.DateTimeField(auto_now_add=True, auto_now=False,
                                verbose_name="Date d'ajout")
    createur = models.ForeignKey('User')
    contributeurs = models.ManyToManyField('User')


    def __str__(self):
        """
        Cette methode que nous definirons dans tous les modeles
        nous permettra de reconnaitre facilement les differents objets que
        nous traiterons plus tard et dans l'administration
        """
        return self.titre

class Picture(models.Model):
    titre = models.CharField(max_length=100)
    image = models.ImageField()
    caption = models.TextField(null=True)
    date = models.DateTimeField(auto_now_add=True, auto_now=False,
                                verbose_name="Date d'ajout")
    createur = models.ForeignKey('User')
    personages = models.ManyToManyField('User')

    def __str__(self):
        """
        Cette methode que nous definirons dans tous les modeles
        nous permettra de reconnaitre facilement les differents objets que
        nous traiterons plus tard et dans l'administration
        """
        return self.titre


class Commentaire(models.Model):
   #se renseigner sur les modèles qui héritent de modèle