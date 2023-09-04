from django.db import models
from django.utils import timezone

from base.models import BaseModel


class Publisher(BaseModel):
    name = models.CharField(max_length=40)
    code = models.CharField(max_length=10)
    started_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name