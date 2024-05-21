
from django.db import models

class Goal(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField(max_length=255)
    sub = models.CharField(max_length=255, null=True, blank=True)  # Allow null and blank values

    def __str__(self):
        return self.title
