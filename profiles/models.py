from django.db import models
from django.contrib.auth.models import User


# Models related to the user profile


class City(models.Model):
    zipcode = models.CharField(max_length=5)
    name = models.CharField(max_length=100)


class Address(models.Model):
    current = models.BooleanField(default=True)
    num = models.IntegerField()
    state = models.CharField(max_length=50)
    street = models.CharField(max_length=100)
    city = models.ForeignKey(City)


class School(models.Model):
    address = models.ForeignKey(Address)
    name = models.CharField(max_length=255)


class StudiesDomain(models.Model):
    name = models.CharField(max_length=255)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.ForeignKey(Address)
    school = models.ForeignKey(School)
    studies_domain = models.ForeignKey(StudiesDomain)

