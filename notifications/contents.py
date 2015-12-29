from forum.models import Thread, Post, ThreadCategory
from .models import NoticeUserPreferences

# Define notice types, notice content types and structures

_NOTICE_TYPES = {
    'post_new': 'forum.models.Thread',
    'post_edit': 'forum.models.Thread',
    'thread_new': 'forum.models.ThreadCategory',
}


def is_regular_type(notice_type):
    return notice_type in _NOTICE_TYPES


def get_related_model(notice_type):
    if is_regular_type(notice_type):
        return _NOTICE_TYPES[notice_type]


class NoticeContent(object):
    notice_types = _NOTICE_TYPES

    def __init__(self, notice_type, emission_date, emitter_user, new_object, parent):
        if not is_regular_type(notice_type):
            print "Wrong notice type when creating content"
            raise Exception
        else:
            self.notice_type = notice_type
        self.emission_date = emission_date
        self.emitter = emitter_user
        self.new_object = new_object
        self.parent = parent

    def get_preference_query(self):
        if isinstance(self.new_object, Post):
            category = self.parent.category
            return NoticeUserPreferences.objects.filter(threads=self.parent, categories=category)
        if isinstance(self.new_object, Thread):
            return NoticeUserPreferences.objects.filter(categories=self.parent)

    def get_object_preference(self, notice_user_preferences):
        if isinstance(self.new_object, Post):
            return notice_user_preferences.threads.get(thread=self.parent)
        if isinstance(self.new_object, Thread):
            return notice_user_preferences.categories.get(category=self.parent)


class OperationPostContent(NoticeContent):
    def __init__(self, notice_type, emission_date, emitter_user, new_post, thread):
        super(OperationPostContent, self).__init__(notice_type, emission_date, emitter_user, new_post, thread)

        if not isinstance(new_post, Post):
            print "Not a Post in operation on  post content init"
            raise TypeError

        if not isinstance(thread, Thread):
            print "Not a thread in operation on post content init"
            raise TypeError


class NewThreadContent(NoticeContent):
    def __init__(self, emission_date, emitter_user, new_thread, category):
        super(NewThreadContent, self).__init__('new_thread', emission_date, emitter_user, new_thread, category)

        if not isinstance(new_thread, Thread):
            print "Not a thread in new thread content init"
            raise TypeError

        if not isinstance(category, ThreadCategory):
            print "Not a catgory in new thread content init"
            raise TypeError
