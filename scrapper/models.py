from django.db import models
from django.utils import timezone


class Job(models.Model):
    uuid = models.CharField(max_length=350, unique=True)
    title = models.CharField(max_length=350)
    location = models.CharField(max_length=250)
    date_posted = models.CharField(max_length=250)
    description = models.CharField(max_length=350)
    link = models.CharField(max_length=1000)
    date_created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return self.title