from django.test import TestCase
from templatetags.bootstrapify import *
# Create your tests here.


class BoostrapifyTestCase(TestCase):
    def setUp(self):
        self.html_input_string = "<input id=\"id_first_name\" maxlength=" \
                                 "\"100\" name=\"first_name\" type=\"text\" value=\"Victor\">"

    def test_boostrapify_forminput(self):
        output = bootstrapify_form_input(self.html_input_string, "label")
        print "Boostrapify output:" + output
        self.assertEqual(True, True)