from django.db import models

class Device(models.Model):
    name = models.CharField(max_length=100, unique=True)
    token = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name