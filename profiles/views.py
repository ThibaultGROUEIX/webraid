from django.views.generic import ListView
from .models import UserProfile


class UserProfilesListView(ListView):

    model = UserProfile
    template_name = 'profiles-list.html'