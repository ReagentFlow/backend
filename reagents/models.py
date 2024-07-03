from django.db import models


class Container(models.Model):
    container_id = models.IntegerField(unique=True, null=False, blank=False)
    name = models.CharField(max_length=100, null=False, blank=False)
    formula = models.CharField(max_length=100, null=False, blank=False)
    mass = models.FloatField(null=False, blank=False)
    volume = models.FloatField(null=False, blank=False)
    density = models.FloatField(null=False, blank=False)
    location = models.CharField(max_length=100, null=False, blank=False)
    precursor = models.BooleanField(null=False, blank=False)
    cas = models.CharField(max_length=100, null=False, blank=False)
    qualification = models.IntegerField(null=False, blank=False)
