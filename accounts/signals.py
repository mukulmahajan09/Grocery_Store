from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Account
from .models import UserProfile

from django.core.mail import EmailMessage
from django.conf import settings


def createProfile(sender, instance, created, **kwargs):
    if created:
        user_profile = UserProfile.objects.create(user=instance)

        # Send email
        mail_subject = 'Welcome To The Kroger Grocery Store!'
        message = 'We are glad you are here! Thank you for choosing Kroger for your grocery needs.'
        to_email = instance.email
        send_email = EmailMessage(mail_subject, message, to=[to_email])
        send_email.send()

#def updateUser(sender, instance, created, **kwargs):
#    UserProfile = instance
#    user = UserProfile.user
#
#    if created == False:
#        name = customer.customer_name
#        name = name.split()
#        first_name = name[0]
#        last_name = ' '.join(name[1:])
#
#        user.first_name = customer.first_name
#        user.last_name = customer.last_name
#        user.email = customer.email
#        user.save()
#
def deleteUser(sender, instance, **kwargs):
        try:
            user = instance.user
            user.delete()
        except:
             pass
        
post_save.connect(createProfile, sender=Account)
#post_save.connect(updateUser, sender=UserProfile)
post_delete.connect(deleteUser, sender=UserProfile)