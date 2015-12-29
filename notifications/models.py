import base64
import cPickle

from django.db import models

from django.db.models.query import QuerySet

from django.contrib.auth.models import User

from profiles.models import UserProfile
from forum.models import Thread, ThreadCategory
import encoding
from encoding import NotificationSettings


class ThreadNoticePreference(models.Model):
    models.ForeignKey(User)
    thread = models.ForeignKey(Thread)
    preferences = models.CharField(max_length=encoding.MAX_SETTINGS_LENGTH)

    def update_preferences(self, preferences):
        self.preferences = preferences
        self.save()


class CategoryNoticePreference(models.Model):
    user = models.ForeignKey(User)
    category = models.ForeignKey(ThreadCategory)
    preferences = models.CharField(max_length=encoding.MAX_SETTINGS_LENGTH)

    def update_preferences(self, preferences):
        self.preferences = preferences
        self.save()


class NoticeUserPreferences(models.Model):
    user = models.OneToOneField(User,
                                to_field='notice_user_preferences')

    default_preferences = models.CharField(max_length=encoding.MAX_SETTINGS_LENGTH,
                                           null=False)
    threads = models.ManyToManyField(ThreadNoticePreference)
    categories = models.ManyToManyField(CategoryNoticePreference)

    class Meta:
        verbose_name = "notification preference per user"
        verbose_name_plural = "notification preferences per user"

    def add_thread(self, thread, preferences):
        prefs = NotificationSettings(preferences)
        thread_notice_preferences = ThreadNoticePreference.objects.get(
            user=self.user,
            thread=thread)
        if thread_notice_preferences is None:
            ThreadNoticePreference(user=self.user, thread=thread, preferences=prefs.get_encoding())
        else:
            thread_notice_preferences.upddate_preferences(prefs.get_encoding())

    def add_category(self, thread_category, preferences):
        prefs = NotificationSettings(preferences)
        category_notice_preferences = CategoryNoticePreference.objects.get(
            user=self.user,
            category_notice_preferences=thread_category)
        if category_notice_preferences is None:
            CategoryNoticePreference(user=self.user,
                                     cateogry=thread_category,
                                     preferences=prefs.get_encoding())
        else:
            category_notice_preferences.update_preferences(prefs.get_encoding())


def follow(user, to_follow):
    user_profile = UserProfile.objects.get(user=user)

    if user_profile.user_notice_preferences is not None:
        prefs = user_profile.user_notice_preferences
    else:
        default_preferences = NotificationSettings().get_encoding()
        prefs = NoticeUserPreferences(user=user_profile, default_preferences=default_preferences).save()

    if prefs is not None:
        if isinstance(to_follow, ThreadCategory):
            prefs.add_thread(to_follow, prefs.default_preferences)
        elif isinstance(to_follow, Thread):
            prefs.add_category(to_follow, prefs.default_preferences)


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


class NoticeQueue(models.Model):
    data = models.TextField()


def enqueue(users, label, extra_context=None, sender=None):
    if extra_context is None:
        extra_context = {}

    if isinstance(users, QuerySet):
        users = [row["pk"] for row in users.values("pk")]
    else:
        users = [user.pk for user in users]
    notices = []

    for user in users:
        notices.append((user, label, extra_context, sender))
    NoticeQueue(data=base64.b64encode(cPickle.dumps(notices))).save()
