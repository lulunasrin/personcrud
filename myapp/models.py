
from django.db import models

class Person(models.Model):
    # Fields for Person
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.name  # Provides a readable string representation of the object
