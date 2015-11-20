from models import UserProfile
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete


# # Create a UserProfile when a User is created
# def create_profile(sender, **kwargs):
#     user = kwargs['instance']
#     if kwargs['created']:
#         user_profile = UserProfile(user=user)
#         user_profile.save()
#
# post_save.connect(create_profile, sender=User)
#
#
# # Delete User when UserProfile is deleted ( UserProfile is automatically deleted
# # when user is deleted
# def delete_user(sender, instance=None, **kwargs):
#     try:
#         instance.user
#     except User.DoesNotExist:
#         pass
#     else:
#         instance.user.delete()
# post_delete.connect(delete_user, sender=UserProfile)
