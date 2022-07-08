from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver

from rest_framework.authtoken.models import Token

# Create your models here.
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Service(models.Model):
    name = models.CharField(max_length=60)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    estimated_time = models.DurationField()


class Hairdresser(models.Model):
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    email = models.EmailField()


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.PROTECT)
    hairdresser = models.ForeignKey(Hairdresser, on_delete=models.PROTECT)
    service = models.ForeignKey(Service, on_delete=models.PROTECT)
    # end time will be calculated via service estimated time.
    start_time = models.DateTimeField()
