import webraid.settings as st


class NotificationManagerRouter(object):
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'notification_manager':
            return st.NOTIFICATION_DB
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'notification_manager':
            return st.NOTIFICATION_DB
        return None

    def allow_syncdb(self, db, model):
        if db == st.NOTIFICATION_DB:
            return model._meta.app_label == 'notification_manager'
        elif model._meta.app_label == 'notification_manager':
            return False
        return None
