from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Organisation(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)

class Camera(models.Model):
    name = models.CharField(max_length = 20)
    org_id = models.ForeignKey(to = Organisation , on_delete = models.CASCADE)

class UserDetails(models.Model):
    user = models.ForeignKey(to = User , on_delete = models.CASCADE )
    org_id = models.ForeignKey(to = Organisation , on_delete = models.CASCADE)
    phone = models.TextField(max_length = 15)
    pic = models.ImageField(upload_to='pictures')
    privilege = models.IntegerField()

class Analytics(models.Model):
    user = models.ForeignKey(to = User , on_delete = models.CASCADE)
    timestamp = models.DateTimeField()
    camera_id = models.ForeignKey(to = Camera , on_delete = models.CASCADE)

class StaffVerification(models.Model):
    token = models.CharField(max_length=50)
    email = models.EmailField()
    visited = models.BooleanField(default = False )







