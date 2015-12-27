from django.db import models

from profiles.models import UserProfile
from forum.models import Thread, ThreadCategory


class NotificationRegistry(models.Model):
    user_profile = models.OneToOneField(UserProfile,
                                        related_name='notification_registry')
    threads = models.ManyToManyField(Thread)
    categories = models.ManyToManyField(ThreadCategory)

    def add_thread(self, thread):
        self.threads.add(thread)
        self.save()

    def add_category(self, thread_category):
        self.categories.add(thread_category)
        self.save()
