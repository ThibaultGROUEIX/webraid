from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from profiles.models import UserProfile


@login_required()
def account_creation(request):
    data = {
        'username': request.user.username
    }
    return render(request, 'account_creation.html', data)


@login_required()
def view_notification_manager(request):
    user_profile = UserProfile.objects.get(user=request.user)
    ntf_reg = user_profile.notification_registry

