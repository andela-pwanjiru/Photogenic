from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from filters import apply_effect


filters = ['blur', 'contour', 'sharpen', 'smooth', 'smooth_more',
           'emboss', 'detail', 'edge_enhance',
           'edge_enhance_more', 'find_edges']


class Images(models.Model):
    """Model for images that have been uploaded"""

    uploader = models.ForeignKey(User, related_name="user")
    image = models.ImageField(upload_to='pics/')
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)


class FilteredImage(models.Model):
    """Base model for photos that have been edited and the preview."""

    image = models.ImageField(upload_to='editedphotos')
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)
    originalimage = models.ForeignKey(Images, related_name="filters", on_delete=models.CASCADE)
    effect = models.CharField(max_length=255)


@receiver(post_save, sender=Images)
def main_effect(sender, instance, **kwargs):
    """Method for applying filters"""
    image = instance.image
    for filter in filters:
        applied = apply_effect(filter, image)
        edited = FilteredImage.objects.create(image=applied, originalimage=instance, effect=filter)
        edited.save()
