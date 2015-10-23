from django.test import TestCase
from models import UserProfile
from django.contrib.auth.models import User


# UserProfile and User are in a one-to-one relation
# Creation of User automatically creates a Userprofile
# Deletion of User / Userprofiles -> deletion of UserProfile / Profile
class UserProfileTestCase(TestCase):

    assert_message_prefix = "UserProfile : "

    def setUp(self):
        User.objects.create(username="zero")
        User.objects.create(username="one")
        User.objects.create(username="two")

    def test_user_profiles_are_created(self):
        zero = User.objects.get(username="zero")

        self.assertTrue(UserProfile.objects.filter(user=zero).count() == 1)

    def test_user_profile_deleted_when_user_deleted(self):
        zero = User.objects.get(username="zero")
        one = User.objects.get(username="one")
        # Delete one of the users
        zero.delete()
        # The corresponding UserProfile should have been deleted
        self.assertEqual(UserProfile.objects.filter(user=zero).count(), 0,
                         self.assert_message_prefix + "UserProfile not deleted when user deleted !")
        # The other UserProfile should still exist
        self.assertEqual(UserProfile.objects.filter(user=one).count(), 1,
                         self.assert_message_prefix + "UserProfile one is missing when after user zero deletion")

    def test_user_deleted_when_user_profile_deleted(self):
        two = User.objects.get(username='two')
        two_profile = UserProfile.objects.get(user=two)
        two_profile.delete()
        # Now the user two should be deleted
        self.assertEqual(User.objects.filter(username='two').count(), 0,
                         self.assert_message_prefix +
                         "The user two has not been deleted when two's profile was deleted !")
