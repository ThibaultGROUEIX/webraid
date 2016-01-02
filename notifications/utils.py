class NotificationContentProviderMixin(object):
    def get_content(self):
        pass


class NotificationParentMixin(object):
    def get_parent_context(self):
        pass


class NotificationContextProviderMixin(object):
    def get_context(self):
        pass
