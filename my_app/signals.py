#this is the signal that is used AFTER the save(action) 
# has taken place in any model(User, in our case)
from django.db.models.signals import post_save
#here User is gonna be the one that sends(sender) the 
# signal which eventually trigger profile creation
from django.contrib.auth.models import User
#this is the reciever which will run the function written below it
from django.dispatch import receiver
from .models import Profile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    #instance : instance of the user, instance of sender model
                #that is, the User model's instance user which 
                #is being created
    #created : if the user is created
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()

    ##############################
    ## check apps.py after this ##
    ##############################

