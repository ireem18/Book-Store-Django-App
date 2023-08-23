from django.db import models
from django.utils import timezone

from writer.models import Writer
from publisher.models import Publisher

from ckeditor_uploader.fields import RichTextUploadingField

class Book(models.Model):
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    writer = models.ForeignKey(Writer, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    subject = models.CharField(max_length=120)
    description = RichTextUploadingField()
    count = models.IntegerField(default=0)
    publisher_date = models.DateTimeField(default=timezone.now)
    page_count = models.IntegerField(default=0)
    isbn = models.CharField(max_length=5)
    active = models.BooleanField(default=True)

    class Meta:
        permissions = (("can_view_book_list", "Can view book list"),
                       ("can_add_book", "Can add book"),
                       ("can_edit_book", "Can edit book"),
                       ("can_delete_book", "Can delete book"))

