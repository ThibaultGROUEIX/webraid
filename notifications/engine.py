from encoding import NotificationSettings
from notification_manager import models as nm_models


def emit_notice(notice_content):
    # Get all the followers for this notice
    users_preferences = notice_content.get_preference_query()
    send_now = []
    send_today = []
    send_week = []
    for user_preferences in users_preferences.all():
        # For each follower, get his preferences and handle notification accordingly
        object_notice_preference = notice_content.get_object_preference(user_preferences)
        prefs = NotificationSettings(encoded_preferences=object_notice_preference.preferences)
        user = object_notice_preference.user
        notice = {'user': user, 'prefs': prefs, 'content': notice_content}
        if prefs.get_dict()['real_time']:
            send_now.append(notice)
        elif prefs.get_dict()['daily']:
            send_today.append(notice)
        elif prefs.get_dict()['weekly']:
            send_week.append(notice)

    for notice in send_now:
        if notice['prefs'].get_dict()['email']:
            nm_models.EnqueuedEmailNotice.queue(
                send_to_user=notice['user'],
                sender_user=notice['content'].emitter,
                notice_label=notice['content'].notice_type,
                content=notice['content'],
                extra_context={'me0': 'jj'}
            )
