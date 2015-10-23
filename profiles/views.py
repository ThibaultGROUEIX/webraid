from django.views.generic import ListView
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import UserProfile


# Views
class UserProfilesListView(ListView):

    model = UserProfile
    template_name = 'profiles-list.html'


def view_logged_out(request):
    return render(request, 'registration/logout.html')


# Mixins
class LoggedInMixin(object):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoggedInMixin, self).dispatch(*args, **kwargs)