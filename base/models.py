from django.db import models
from django.apps import apps


class ActiveManager(models.Manager):
    def active(self):
        return self.model.objects.filter(active=True)


class BaseModel(models.Model):
    active = models.BooleanField(default=True)
    objects = ActiveManager()

    class Meta:
        abstract = True

    def deactive(self, type=''):
        self.active = False
        self.save()
        Book = apps.get_model('books', 'Book')
        Writer = apps.get_model('writer', 'Writer')
        books = Book.objects.active()

        if type == 'publisher':
            books = books.filter(publisher=self)
            writers = Writer.objects.active().filter(publisher=self)
            for book in books:
                book.deactive()
            for writer in writers:
                writer.deactive()
        elif type == 'writer':
            books = books.filter(writer=self)
            for book in books:
                book.deactive()
