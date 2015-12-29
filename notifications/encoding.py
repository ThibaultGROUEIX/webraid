# Preferences are encoded on a string with at most 10 characters
MAX_SETTINGS_LENGTH = 10

ENCODING = {
    'in_app': 'a',
    'email': 'e',
    'real_time': 'r',
    'daily': 'd',
    'weekly': 'w',
    'use_defaults': '0'
}

INVERSE_ENCODING = {v: k for k, v in ENCODING.iteritems()}


def encode_settings(kwargs):
    s = ""
    for k, v in kwargs.iteritems():
        if v is True:
            s += ENCODING.get(k, '')
    return s


class NotificationSettings(object):
    DEFAULT_NOTIFICATION_SETTINGS = {
        'in_app': True,
        'email': True,
        'real_time': True,
        'daily': False,
        'weekly': False,
        'use_defaults': False
    }

    def length_ok(self):
        return self._encoded_settings.__len__() <= MAX_SETTINGS_LENGTH

    def __init__(self, preferences=None, encoded_preferences=None):
        if preferences is None:
            if encoded_preferences is not None:
                self.update_from_string(encoded_preferences)
            else:
                self.update_from_dict(self._settings)
        else:
            self._settings = preferences
            self._encoded_settings = encode_settings(self._settings)
            # Normalize
            self.update_from_string(self._encoded_settings)

        if not self.length_ok():
            raise AttributeError

    def update_from_dict(self, settings):
        self._settings = settings
        self._encoded_settings = encode_settings(settings)
        # Normalize
        self.update_from_string(self._encoded_settings)

    def update_from_string(self, encoded_settings):
        self._encoded_settings = encoded_settings
        if not self.length_ok():
            raise AttributeError
        for c in INVERSE_ENCODING:
            if c in encoded_settings:
                self._settings[INVERSE_ENCODING[c]] = True
            else:
                self._settings[INVERSE_ENCODING[c]] = False

    def get_encoding(self):
        return self._encoded_settings

    def get_dict(self):
        return self._settings

    def __str__(self):
        return unicode(self._encoded_settings)
