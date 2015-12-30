from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from profiles.models import UserProfile
from forum.models import Thread, ThreadCategory
from models import NoticeUserPreferences


@login_required()
def follow(request, slug, obj_to_follow_type):
    try:
        notice_user_preference = NoticeUserPreferences.objects.get(user=request.user)
    except NoticeUserPreferences.DoesNotExist:
        notice_user_preference = NoticeUserPreferences.create_user_preferences(request.user)

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


def unfollow(request, slug, obj_to_unfollow_type):
    try:
        notice_user_preferences = NoticeUserPreferences.objects.get(user=request.user)
    except NoticeUserPreferences.DoesNotExist:
        NoticeUserPreferences.create_user_preferences(request.user)
        return redirect(request.META.get('HTTP_REFERER'))

    if obj_to_unfollow_type is 'thread':
        elt = Thread.objects.get(slug=slug)
    elif obj_to_unfollow_type is 'category':
        elt = ThreadCategory.objects.get(slug=slug)
    else:
        elt = None
    notice_user_preferences.remove_element(elt)

    return redirect(request.META.get('HTTP_REFERER'))


@login_required()
def unfollow_thread(request, slug):
    return unfollow(request, slug, 'thread')


@login_required()
def unfollow_category(request, slug):
    return unfollow(request, slug, 'category')


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
