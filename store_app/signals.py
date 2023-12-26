from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from django.contrib.auth.models import User
from .models import Customer

from django.core.mail import send_mail
from django.conf import settings

def createCustomer(sender, instance, created, **kwargs):
    if created:
        user = instance
        full_name = f"{user.first_name} {user.last_name}"
        
        customer = Customer.objects.create(
            user=user,
            customer_name=full_name,
            email=user.email,
        )

        #subject = 'Welcome To The Kroger Grocery Store!'
        #message = 'We are glad you are here! Thank you for choosing Kroger for your grocery needs.'
#
        #send_mail(
        #    subject,
        #    message,
        #    settings.EMAIL_HOST_USER,
        #    [Customer.email],
        #    fail_silently=False,
        #)

def updateUser(sender, instance, created, **kwargs):
    customer = instance
    user = customer.user

    if created == False:
        name = customer.customer_name
        name = name.split()
        first_name = name[0]
        last_name = ' '.join(name[1:])

        user.first_name = customer.first_name
        user.last_name = customer.last_name
        user.email = customer.email
        user.save()

def deleteUser(sender, instance, **kwargs):
        try:
            user = instance.user
            user.delete()
        except:
             pass
        
post_save.connect(createCustomer, sender=User)
post_save.connect(updateUser, sender=Customer)
post_delete.connect(deleteUser, sender=Customer)