from django.views.generic import ListView
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.exceptions import ObjectDoesNotExist

from forum.models import Post, Thread
from forms import DetailedUserProfileForm, CityForm, AddressForm
from .models import UserProfile, Address, City, CallingCode


# Views
class UserProfilesListView(ListView):
    model = UserProfile
    template_name = 'profiles-list.html'


def home_redirect(request):
    return redirect(reverse('dashboard'))


def view_logged_out(request):
    return render(request, 'logout.html')


def dashboard(request):
    user = request.user
    post_and_answers = Post.get_last_posts_by_author_with_answers(user, posts_limit=5, answers_limit=3)
    last_threads_posted_in = Thread.get_last_threads_posted_in_with_posts(threads_limit=5, posts_limit=2)
    return render(request, 'dashboard.html',
                  {'user': user,
                   'posts': post_and_answers,
                   'threads_last': last_threads_posted_in})


@login_required
def detailed_user_profile_form(request, id=None):
    init_data = {}
    user = request.user
    user_profile = UserProfile.objects.get(user_id=request.user.id)
    if request.method == 'POST':
        user_profile_form = DetailedUserProfileForm(request.POST, request.FILES)

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

            # Check if we can get this city
            # If the city doesn't exist, we try to create it, but data may be incomplete
            try:
                city = City.objects.get(**city_data)
            except ObjectDoesNotExist:
                try:
                    city = CityForm(data=city_data).save()
                except ValueError:
                    city = None

            if city is not None:
                address_data = {
                    'num': user_profile_form.cleaned_data['num'],
                    'street': user_profile_form.cleaned_data['street'],
                    'city': city.pk,
                }

                try:
                    address = Address.objects.get(**address_data)
                except ObjectDoesNotExist:
                    try:
                        address = AddressForm(data=address_data).save()
                    except ValueError:
                        address = None
            else:
                address = None

            user_profile.address = address
            user_profile.dialcode = user_profile_form.cleaned_data['dialcode']
            user_profile.phone_number = user_profile_form.cleaned_data['phone_number']
            user_profile.school = user_profile_form.cleaned_data['school']
            user_profile.studies_domain = user_profile_form.cleaned_data['studies_domain']

            # Profile picture
            if 'profile_picture' in user_profile_form.changed_data:
                import Image as Pil
                import StringIO, time
                from django.core.files.uploadedfile import InMemoryUploadedFile

                profile_pic = Pil.open(request.FILES.get('profile_picture'))
                profile_pic.thumbnail((200, 200), Pil.ANTIALIAS)
                ppic_io = StringIO.StringIO()
                profile_pic.save(ppic_io, request.FILES['profile_picture'].content_type.split('/')[-1].upper())
                ppic_filename = request.user.username + '_avatar_' + str(int(time.time()))
                ppic_file = InMemoryUploadedFile(ppic_io,
                                                 u"profile_picture",
                                                 ppic_filename,
                                                 request.FILES['profile_picture'].content_type,
                                                 ppic_io.len,
                                                 None)
                user_profile.profile_picture = ppic_file

            user_profile.save()

            return redirect(reverse('profiles-list'))

        else:
            return render(request,
                          'forms/detailed_userprofile_form.html',
                          {'form': user_profile_form})

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
        init_data['dialcode'] = CallingCode.objects.get(pk=user_profile.dialcode.pk)

    if user_profile.profile_picture is not None:
        init_data['profile_picture'] = user_profile.profile_picture

    return render(request, 'forms/detailed_userprofile_form.html',
                  {'form': DetailedUserProfileForm(initial=init_data)})


def view_profile(request, user_id):
    user_profile = UserProfile.objects.get(user_id=user_id)
    pic = user_profile.profile_picture
    pwas = Post.get_last_posts_by_author_with_answers(user_profile.user, posts_limit=5, answers_limit=2)
    return render(request,
                  'profile-detail.html',
                  {'user_profile': user_profile,
                   'pwas': pwas,
                   'pic': pic,
                   }
                  )


# Mixins
class LoggedInMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoggedInMixin, self).dispatch(*args, **kwargs)
