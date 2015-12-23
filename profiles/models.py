import json

from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField


# Models related to the user profile
class CallingCode(models.Model):
    calling_code = models.IntegerField()
    country = CountryField(default='None')

    def __str__(self):
        return self.country.name.__str__() + " - (+" + str(self.calling_code) + ")"

    @staticmethod
    def populate_from_json(json_file):
        with open(json_file, 'r') as data_file:
            data = json.load(data_file)

        for country in data:
            country_iso2 = country['iso']
            country_dialcode = country['prefix']
            CallingCode(country=country_iso2, calling_code=country_dialcode).save()


class City(models.Model):
    zipcode = models.CharField(max_length=5)
    name = models.CharField(max_length=100)
    country = CountryField(blank_label='(select country)')

    def __str__(self):
        return self.name + " (" + self.zipcode + ") - " + self.country.name.__str__()


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
    dialcode = models.ForeignKey(CallingCode, null=True)
    phone_number = models.CharField(max_length=100, null=True)
    school = models.ForeignKey(School, null=True)
    studies_domain = models.ForeignKey(StudiesDomain, null=True)

    # Profile pictures stored by year and month
    profile_picture = models.ImageField(upload_to='profiles/profile_pics/%Y/%m',
                                        max_length=150,
                                        null=True)

    def __str__(self):
        return self.user.__str__()

