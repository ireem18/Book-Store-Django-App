from django.db import models
from django.utils import timezone

from base.models import BaseModel


class Publisher(BaseModel):
    name = models.CharField(max_length=40)
    code = models.CharField(max_length=10)
    started_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    def deactive(self, obj):
        super().deactive(obj)
        books = obj.books.filter(active=True)
        writers = obj.writers.filter(active=True)
        for book in books:
            super().deactive(book)
        for writer in writers:
            super().deactive(writer)

