from django import forms
from django_countries.fields import LazyTypedChoiceField
from django_countries import countries

from models import City, Address, StudiesDomain, School, UserProfile, CallingCode


# Default base forms
class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ['name', 'zipcode', 'country']


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['num', 'street', 'city']


class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ['name', 'address']


class StudiesDomainForm(forms.ModelForm):
    class Meta:
        model = StudiesDomain
        fields = '__all__'


# Detailed form : you can create user's address, school, and change name in it.
class DetailedUserProfileForm(forms.Form):
    # User fields
    user_name = forms.CharField(max_length=100)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField(label="Ton adresse mail")
    confirm_email = forms.EmailField(label="Confirme ton adresse mail")
    # Address fields
    num = forms.IntegerField(initial='address__number',
                             required=False)
    street = forms.CharField(max_length=255,
                             required=False)
    city = forms.CharField(max_length=255,
                           required=False)
    zipcode = forms.CharField(max_length=100,
                              required=False)
    country = LazyTypedChoiceField(choices=countries,
                                   required=False)
    # Phone number
    dialcode = forms.ModelChoiceField(queryset=CallingCode.objects.all(),
                                      required=False)

    phone_number = forms.CharField(max_length=100,
                                   required=False)
    # School field
    school = forms.ModelChoiceField(queryset=School.objects.all(),
                                    required=False)
    # Studies domain
    studies_domain = forms.ModelChoiceField(queryset=StudiesDomain.objects.all(),
                                            required=False,
                                            help_text="Choisis ton domaine d'etudes",
                                            initial='studies_domain')

    profile_picture = forms.FileField(required=False)

    def clean(self):

        # Check that the two email fields are the same
        if self.cleaned_data['email'] != self.cleaned_data['confirm_email']:
            raise forms.ValidationError("Email and email confirmation do not match")

        super(DetailedUserProfileForm, self).clean()


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = '__all__'
