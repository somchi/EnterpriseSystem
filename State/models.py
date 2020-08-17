from __future__ import unicode_literals

from django.db import models

class State(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Country(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class LGA(models.Model):
    state = models.ForeignKey(State, null=True)
    name = models.CharField(max_length=30)
    
    def __str__(self):
        return self.name
