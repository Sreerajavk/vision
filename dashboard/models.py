from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Organisation(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)

    def __str__(self):
        return str(self.id)

class Camera(models.Model):
    name = models.CharField(max_length = 20)
    org_id = models.ForeignKey(to = Organisation , on_delete = models.CASCADE)

class UserDetails(models.Model):
    user = models.ForeignKey(to = User , on_delete = models.CASCADE )
    org_id = models.ForeignKey(to = Organisation , on_delete = models.CASCADE)
    phone = models.TextField(max_length = 15)
    pic = models.ImageField(upload_to='pictures' , null=True)
    privilege = models.IntegerField()

class Analytics(models.Model):
    user = models.ForeignKey(to = User , on_delete = models.CASCADE)
    timestamp = models.DateTimeField()
    camera_id = models.ForeignKey(to = Camera , on_delete = models.CASCADE)

class StaffVerification(models.Model):
    token = models.CharField(max_length=50)
    email = models.EmailField()
    visited = models.BooleanField(default = False )

class CandidatePics(models.Model):
    user = models.ForeignKey(to = User , on_delete = models.CASCADE)
    images = models.FileField(upload_to = 'candidates')







