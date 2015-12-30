from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from profiles.models import UserProfile
from forum.models import Thread, ThreadCategory
from models import NoticeUserPreferences
from encoding import NotificationSettings


@login_required()
def follow(request, slug, obj_to_follow_type):
    try:
        notice_user_preference = NoticeUserPreferences.objects.get(user=request.user)
    except NoticeUserPreferences.DoesNotExist:
        settings = NotificationSettings(preferences=NotificationSettings.DEFAULT_NOTIFICATION_SETTINGS)
        notice_user_preference = NoticeUserPreferences(
            user=request.user,
            default_preferences=settings.get_encoding()
        )
        notice_user_preference.save()

    if obj_to_follow_type is 'thread':
        element = Thread.objects.get(slug=slug)
        notice_user_preference.add_thread(element)

    elif obj_to_follow_type is 'category':
        element = ThreadCategory.objects.get(slug=slug)
        notice_user_preference.add_category(element)

    return redirect(request.META.get('HTTP_REFERER'))


@login_required()
def follow_thread(request, thread_slug):
    return follow(request, thread_slug, 'thread')


@login_required()
def follow_category(request, category_slug):
    return follow(request, category_slug, 'category')


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
