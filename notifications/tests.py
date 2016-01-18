from django.test import TestCase

from encoding import NotificationSettings


# Create your tests here.

class NotificationEncodingTestCase(TestCase):
    def test_default_encoding(self):
        encoded_settings = "aer"
        prefs = NotificationSettings(encoded_preferences=encoded_settings)
        self.assertEqual(prefs.get_encoding(), "aer")
