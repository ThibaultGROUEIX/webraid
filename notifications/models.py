from django.db import models
from django.contrib.auth.models import User

from profiles.models import UserProfile
from forum.models import Thread, ThreadCategory
import encoding
from encoding import NotificationSettings


class ThreadNoticePreference(models.Model):
    user = models.ForeignKey(User)
    nothing = models.TextField()
    thread = models.ForeignKey(Thread)
    preferences = models.CharField(max_length=encoding.MAX_SETTINGS_LENGTH)

    class Meta:
        verbose_name = "Thread Notice Preference (user)"

    def update_preferences(self, preferences):
        self.preferences = preferences
        self.save()


class CategoryNoticePreference(models.Model):
    user = models.ForeignKey(User)
    category = models.ForeignKey(ThreadCategory)
    preferences = models.CharField(max_length=encoding.MAX_SETTINGS_LENGTH)

    class Meta:
        verbose_name = "Category Notice Preference (user)"

    def update_preferences(self, preferences):
        self.preferences = preferences
        self.save()


class NoticeUserPreferences(models.Model):
    user = models.OneToOneField(User,
                                related_name='notice_user_preferences')

    default_preferences = models.CharField(max_length=encoding.MAX_SETTINGS_LENGTH,
                                           null=False)
    threads = models.ManyToManyField(ThreadNoticePreference)
    categories = models.ManyToManyField(CategoryNoticePreference)

    class Meta:
        verbose_name = "Notifications preferences (user)"
        verbose_name_plural = "notification preferences (users)"

    @staticmethod
    def create_user_preferences(user):
        settings = NotificationSettings(preferences=NotificationSettings.DEFAULT_NOTIFICATION_SETTINGS)
        notice_user_preference = NoticeUserPreferences(
            user=user,
            default_preferences=settings.get_encoding()
        )
        notice_user_preference.save()

        return notice_user_preference

    def prefs_or_defaults(self, preferences=None):
        try:
            if preferences is None:
                if self.default_preferences is None:
                    print "Default preferences not provided"
                    prefs = NotificationSettings(
                        preferences=NotificationSettings.DEFAULT_NOTIFICATION_SETTINGS)
                else:
                    prefs = NotificationSettings(encoded_preferences=self.default_preferences)
            else:
                prefs = NotificationSettings(preferences=preferences)
        except AttributeError:
            print "Prefs or default : bad preferences"
            print AttributeError
            return None

        return prefs

    def add_thread(self, thread, preferences=None):
        prefs = self.prefs_or_defaults(preferences)
        try:
            thread_notice_preferences = ThreadNoticePreference.objects.get(
                user=self.user,
                thread=thread)
        except ThreadNoticePreference.DoesNotExist:
            thread_notice_preferences = ThreadNoticePreference(
                user=self.user,
                thread=thread,
                preferences=prefs.get_encoding()
            )
            thread_notice_preferences.save()
            self.threads.add(thread_notice_preferences)

        thread_notice_preferences.update_preferences(prefs.get_encoding())

    def add_category(self, thread_category, preferences=None):
        prefs = self.prefs_or_defaults(preferences)
        try:
            category_notice_preferences = CategoryNoticePreference.objects.get(
                user=self.user,
                category_notice_preferences=thread_category)
        except CategoryNoticePreference.DoesNotExist:
            category_notice_preferences = CategoryNoticePreference(
                user=self.user,
                category=thread_category,
                preferences=prefs.get_encoding()
            )
            category_notice_preferences.save()
            self.categories.add(category_notice_preferences)
        else:
            category_notice_preferences.update_preferences(prefs.get_encoding())

    def remove_element(self, element):
        element_notice_prefs = None
        if isinstance(element, Thread):
            element_notice_prefs = self.threads.all().get(thread=element)
        elif isinstance(element, ThreadCategory):
            element_notice_prefs = self.categories.all().get(category=element)
        element_notice_prefs.delete()


class NoticeType(models.Model):
    label = models.CharField(max_length=40)
    display = models.CharField(max_length=50)
    description = models.CharField(max_length=100)

    class Meta:
        verbose_name = "notification type"
        verbose_name_plural = "notification types"

    @classmethod
    def create(cls, label, display, description, default=2, verbosity=1):
        """
        Creates a new NoticeType.
        This is intended to be used by other apps as a post_syncdb management step.
        """
        try:
            notice_type = cls._default_manager.get(label=label)
            updated = False
            if display != notice_type.display:
                notice_type.display = display
                updated = True
            if description != notice_type.description:
                notice_type.description = description
                updated = True
            if default != notice_type.default:
                notice_type.default = default
                updated = True
            if updated:
                notice_type.save()
                if verbosity > 1:
                    print("Updated %s NoticeType" % label)
        except cls.DoesNotExist:
            cls(label=label, display=display, description=description, default=default).save()
            if verbosity > 1:
                print("Created %s NoticeType" % label)
