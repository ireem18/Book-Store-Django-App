from django.db import models
from django.utils import timezone

class Publisher(models.Model):
    name = models.CharField(max_length=40)
    code = models.CharField(max_length=10)
    started_date = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name