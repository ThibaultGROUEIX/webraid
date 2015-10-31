from django.views.generic import ListView
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from forms import DetailedUserProfileForm, CityForm, AddressForm
from .models import UserProfile, Address, City, CallingCode


# Views
class UserProfilesListView(ListView):
    model = UserProfile
    template_name = 'profiles-list.html'


def home_redirect(request):
    return redirect(reverse('profiles-list'))


def view_logged_out(request):
    return render(request, 'registration/logout.html')


def detailed_user_profile_form(request, id=None):
    init_data = {}
    user = request.user
    user_profile = UserProfile.objects.get(user_id=request.user.id)

    if request.method == 'POST':
        user_profile_form = DetailedUserProfileForm(request.POST)

        if user_profile_form.is_valid():
            # User info
            user.username = user_profile_form.cleaned_data['user_name']
            user.first_name = user_profile_form.cleaned_data['first_name']
            user.last_name = user_profile_form.cleaned_data['last_name']
            user.email = user_profile_form.cleaned_data['email']
            user.save(force_insert=False,
                      force_update=True,
                      update_fields=('username', 'first_name', 'last_name', 'email'))
            # Address : address and city
            city_data = {
                'name': user_profile_form.cleaned_data['city'],
                'zipcode': user_profile_form.cleaned_data['zipcode'],
                'country': user_profile_form.cleaned_data['country']
            }
            city = CityForm(data=city_data).save()

            address_data = {
                'num': user_profile_form.cleaned_data['num'],
                'street': user_profile_form.cleaned_data['street'],
                'city': city.pk,
            }

            address = AddressForm(data=address_data).save()

            user_profile.address = address
            user_profile.phone_number = user_profile_form.cleaned_data['phone_number']
            user_profile.school = user_profile_form.cleaned_data['school']
            user_profile.studies_domain = user_profile_form.cleaned_data['studies_domain']

            user_profile.save()

            return redirect(reverse('profiles-list'))

    else:
        init_data = {
            'user_name': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'confirm_email': user.email
        }

        if user_profile.address is not None:
            user_address = Address.objects.get(pk=user_profile.address.pk)
            user_city = City.objects.get(pk=user_address.city.pk)
            init_data.update({
                'num': user_address.num,
                'street': user_address.street,
                'city': user_city.name,
                'zipcode': user_city.zipcode,
                'country': user_city.country,
                'phone_number': user_profile.phone_number,
                'school': user_profile.school,
                'studies_domain': user_profile.studies_domain,
            })
        if user_profile.dialcode is not None:
            init_data.update({'dialcode': CallingCode.objects.get(pk=user_profile.dialcode.pk).calling_code})

    return render(request, 'forms/detailed_userprofile_form.html',
                  {'form': DetailedUserProfileForm(initial=init_data)})


# Mixins
class LoggedInMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoggedInMixin, self).dispatch(*args, **kwargs)
