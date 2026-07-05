from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile


@receiver(post_save, sender=User)
def creer_ou_maj_profile(sender, instance, created, **kwargs):
    """Crée automatiquement un Profile lorsqu'un User est créé."""
    if created:
        Profile.objects.get_or_create(user=instance)
