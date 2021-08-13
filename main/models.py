from phonenumber_field.modelfields import PhoneNumberField

from django.db import models
from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.urls import reverse


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True, default=None, related_name='profile')
    phone = PhoneNumberField(blank=True, null=True, default=None)
    address = models.CharField(max_length=80, blank=True, null=True, default=None)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def get_absolute_url(self):
        return reverse('account', kwargs={'pk': self.pk})
        
    def get_update_url(self):
        return reverse('edit_account', kwargs={'pk': self.pk})
        
    def get_delete_url(self):
        return reverse('delete_account', kwargs={'pk': self.pk})
        
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, created, **kwargs):
    instance.profile.save()
    
@receiver(post_delete, sender=Profile)
def delete_user(sender, instance, **kwargs):
    instance.user.delete()
