from django import forms

from models import City, Address, StudiesDomain, School, UserProfile


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
    last_name = forms.CharField(max_length=100, initial='lname')
    email = forms.EmailField(label="Ton adresse mail", initial='email')
    confirm_email = forms.EmailField(label="Confirme ton adresse mail", initial='email')
    # Address fields
    num = forms.IntegerField(initial='address__number')
    street = forms.CharField(max_length=255, initial='address__street')
    city = forms.CharField(max_length=255, initial='address__city__name')
    zipcode = forms.CharField(max_length=100, initial='address__city__zipcode')
    country = forms.CharField(max_length=100, initial='address__city__country')
    # School field
    school = forms.ModelChoiceField(queryset=School.objects.all(),
                                    required=False,
                                    initial='school')
    # Studies domain
    studies_domain = forms.ModelChoiceField(queryset=StudiesDomain.objects.all(),
                                            required=False,
                                            help_text="Choisis ton domaine d'etudes",
                                            initial='studies_domain')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = '__all__'
