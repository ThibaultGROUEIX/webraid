# Preferences are encoded on a string with at most 10 characters
MAX_SETTINGS_LENGTH = 10

ENCODING = {
    'in_app': 'a',
    'email': 'e',
    'real_time': 'r',
    'daily': 'd',
    'weekly': 'w'
}

INVERSE_ENCODING = {v: k for k, v in ENCODING.iteritems()}


def encode_settings(kwargs):
    s = ""
    for k, v in kwargs.iteritems():
        if v is True:
            s += ENCODING.get(k, '')
    return s


class NotificationSettings:
    DEFAULT_NOTIFICATION_SETTINGS = {
        'in_app': True,
        'email': True,
        'real_time': True,
    }

    def length_ok(self):
        return self._encoded_settings.__len__() <= MAX_SETTINGS_LENGTH

    def __init__(self, preferences=None):
        if preferences is None:
            self._settings = self.DEFAULT_NOTIFICATION_SETTINGS
        else:
            self._settings = preferences
        self._encoded_settings = encode_settings(self._settings)
        if not self.length_ok():
            raise AttributeError

    def update_from_dict(self, settings):
        self._settings = settings
        self._encoded_settings = encode_settings(settings)

    def update_from_string(self, encoded_settings):
        self._encoded_settings = encoded_settings
        if not self.length_ok():
            raise AttributeError
        for c in encoded_settings:
            if INVERSE_ENCODING[c] is not None:
                self._settings[INVERSE_ENCODING[c]] = True

    def get_encoding(self):
        return self._encoded_settings

    def get_dict(self):
        return self._settings

    def __str__(self):
        return unicode(self._encoded_settings)
