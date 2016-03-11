from encoding import NotificationSettings
from notification_manager import models as nm_models


def emit_notice(notice_content):
    """
    Dispatch a notice content to all backends queues and receivers.
    :param notice_content: an instance of a class extending a NotificationContextProviderMixin
    """
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
        # Don't send the notification if the user is the emitter !
        if user != notice_content.emitter:
            notice = {'user': user, 'prefs': prefs, 'content': notice_content}
            in_rt = prefs.get_dict()['real_time']
            in_daily_digest = prefs.get_dict()['daily']
            in_weekly_digest = prefs.get_dict()['weekly']
            nm_models.EnqueuedEmailNotice.enqueue(notice['user'],
                                                notice['content'],
                                                in_rt,
                                                in_daily_digest,
                                                in_weekly_digest)
