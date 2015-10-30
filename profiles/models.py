from django.db import models
from django.contrib.auth.models import User


# Models related to the user profile


class City(models.Model):
    zipcode = models.CharField(max_length=5)
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=255, default='None')

    def __str__(self):
        return self.name + " (" + self.zipcode + ") - " + self.country


class Address(models.Model):
    num = models.IntegerField()
    street = models.CharField(max_length=255)
    city = models.ForeignKey(City)

    def __str__(self):
        return ", ".join([
            unicode(self.num),
            self.street,
            self.city.__str__()
        ])


class School(models.Model):
    address = models.ForeignKey(Address)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class StudiesDomain(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    # Relations
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name='user_profile')
    address = models.ForeignKey(Address, null=True)
    school = models.ForeignKey(School, null=True)
    studies_domain = models.ForeignKey(StudiesDomain, null=True)

    def __str__(self):
        return self.user.__str__()
