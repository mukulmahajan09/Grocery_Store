#from django.db.models.signals import post_save, post_delete
#from django.dispatch import receiver
#
#from .models import Account
#from .models import UserProfile
#
#from django.core.mail import send_mail
#from django.conf import settings
#
#def createCustomer(sender, instance, created, **kwargs):
#    if created:
#        Account = instance
#        full_name = f"{Account.first_name} {Account.last_name}"
#        
#        user = UserProfile.objects.create(
#            user=user,
#            user_full_name=full_name,
#        )
#
#        #subject = 'Welcome To The Kroger Grocery Store!'
#        #message = 'We are glad you are here! Thank you for choosing Kroger for your grocery needs.'
##
#        #send_mail(
#        #    subject,
#        #    message,
#        #    settings.EMAIL_HOST_USER,
#        #    [Customer.email],
#        #    fail_silently=False,
#        #)
#
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
#def deleteUser(sender, instance, **kwargs):
#        try:
#            user = instance.Account
#            user.delete()
#        except:
#             pass
#        
#post_save.connect(createCustomer, sender=Account)
#post_save.connect(updateUser, sender=UserProfile)
#post_delete.connect(deleteUser, sender=UserProfile)