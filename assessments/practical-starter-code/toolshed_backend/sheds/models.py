from django.contrib.auth.models import User
from django.db import models


class Shed(models.Model):
    name = models.CharField(max_length=200)
    suburb = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sheds")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Tool(models.Model):
    shed = models.ForeignKey(Shed, on_delete=models.CASCADE, related_name="tools")
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.name