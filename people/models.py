from __future__ import unicode_literals

from django.db import models


# Create your models here.
class Person(models.Model):
    fname = models.CharField(max_length=16)
    lname = models.CharField(max_length=16)
    email_address = models.EmailField(default=None)
    phone_number = models.CharField(max_length=16, default=None)
