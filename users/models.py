from django.db import models
from django.contrib.auth.models import User
# from .models import UserProfile  # ✅ Correct import


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField()
    height = models.FloatField()
    weight = models.FloatField()
    bmi = models.FloatField(blank=True, null=True)
    gender = models.CharField(max_length=20, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    activity_level = models.CharField(max_length=50)
    medical_conditions = models.TextField(blank=True, null=True)  



    def __str__(self):
        return self.user.username


class ScannedFood(models.Model):
    name = models.CharField(max_length=255)
    ingredients = models.TextField()