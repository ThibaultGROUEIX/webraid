class NotificationContentProviderMixin(object):
    """
        Provides the content of a notice such as a Post, a Thread
    """

    def get_content(self):
        pass


class NotificationParentMixin(object):
    """
        Provides the parents of a notice, such a a Thread for a Post notice
    """

    def get_parent_context(self):
        pass


class NotificationContextProviderMixin(object):
    """
        Wraps content and metadata about the notice,
    """

    def __init__(self, emission_date, emitter_user, new_object, notice_type, parent):
        """
        :param emission_date:date of emission of the notice
        :param emitter_user: user emitting the notice
        :param new_object: NotificationContentProviderMixin instance ,
            the object for which we provide a notice
        :param notice_type: a custom notice type
        :param parent: NotificationParentMixin,
            the parent object of the notice
        """
        self.emission_date = emission_date
        self.emitter = emitter_user
        self.new_object = new_object
        self.notice_type = notice_type
        self.parent = parent

        # Check that the new object is a notification content provider
        if not isinstance(self.new_object, NotificationContentProviderMixin):
            print "The object passed to NoticeContent is not a notification source"
            raise BadNotificationContextInit()

        # Check that the parent is a notification parent mixin

        if not isinstance(self.parent, NotificationParentMixin):
            print "The object passed to NoticeContent is not a notification parent"
            raise BadNotificationContextInit()

    def get_content(self):
        return self.new_object.get_content()

    def get_context(self):
        return {
            'emitter': {
                'email': self.emitter.email,
                'first_name': self.emitter.first_name,
                'last_name': self.emitter.last_name,
                'username': self.emitter.username
            },
            'notice_type': self.notice_type,
            'date': self.emission_date,
            'parent': self.parent.get_parent_context()
        }


class BadNotificationContextInit(Exception):
    def __init__(self, args, *kwargs):
        super(BadNotificationContextInit, self).__init__(args, kwargs)

    def __str__(self):
        s = "An error occurred during the inititalization of the NotificationContextProvider\n"
        if self.message is not None:
            s += self.message
        return s
