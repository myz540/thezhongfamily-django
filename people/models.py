from django.db import models
from django.forms import ModelForm
from django.contrib.admin import widgets
from django.forms.extras import SelectDateWidget
from django import forms
import datetime


# Create your models here.
class Person(models.Model):
    fname = models.CharField(max_length=16)
    lname = models.CharField(max_length=16)
    email_address = models.EmailField(default=None)
    picture = models.ImageField()

    def __str__(self):
        return u"Name: %s %s" % (self.fname, self.lname)

class WallPost(models.Model):
    poster_name = models.CharField(max_length=32)
    post_dt = models.DateTimeField(auto_now_add=True)
    post_content = models.CharField(max_length=512)

    def __str__(self):
        return u"Posted by %s on %s" % (self.poster_name, self.post_dt)

class WallPostForm(ModelForm):

    class Meta:
        model = WallPost
        fields = "__all__"
