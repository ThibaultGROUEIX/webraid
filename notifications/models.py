import base64
import cPickle

from django.db import models

from django.db.models.query import QuerySet

from profiles.models import UserProfile
from forum.models import Thread, ThreadCategory


class NoticeUserPreferences(models.Model):
    user_profile = models.OneToOneField(UserProfile,
                                        related_name='notice_user_preferences')
    threads = models.ManyToManyField(Thread)
    categories = models.ManyToManyField(ThreadCategory)

    class Meta:
        verbose_name = "notification preference per user"
        verbose_name_plural = "notification preferences per user"

    def add_thread(self, thread):
        self.threads.add(thread)
        self.save()

    def add_category(self, thread_category):
        self.categories.add(thread_category)
        self.save()


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
        This is intended to be used by other apps as a post_syncdb manangement step.
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


def send_now(users, label, extra_context=None, sender=None, scoping=None):
    notice_type = NoticeType.objects.get(label=label)

    for user in users:
        return user


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
