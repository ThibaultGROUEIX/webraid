from models import NoticeType, NoticeUserPreferences
from encoding import NotificationSettings
import contents


def emit_notice(notice_content):
    # Get all the followers for this notice
    user_preferences_list = notice_content.get_preference_query()
    for user_preferences in user_preferences_list:
        object_notice_preference = notice_content.get_object_preference(user_preferences)
        prefs = NotificationSettings(encoded_preferences=object_notice_preference.preferences)

def send(content, label):
    if not contents.is_regular_type(type):
        raise Exception
    notice_type = NoticeType.objects.get(label=label)
    notice_model = contents.get_related_model(notice_type)
    notice_model_instance = notice_model.objects.get(slug=content['origin_id'])

    for user_prefs in NoticeUserPreferences.objects.iterator():
        user_prefs.get_prefs(notice_model_instance)
