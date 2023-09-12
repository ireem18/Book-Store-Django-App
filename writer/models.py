from django.core.validators import MinValueValidator
from django.db import models
from publisher.models import Publisher

from base.models import BaseModel

categories = (
    ('social', 'Social'),
    ('historical', 'Historical'),
    ('adventure', 'Adventure'),
    ('psychological', 'Psychological'),
    ('espionage', 'Espionage'),
    ('detective', 'Detective'),
    ('modern', 'Modern'),
)


class Writer(BaseModel):
    name = models.CharField(max_length=40)
    surname = models.CharField(max_length=40)
    age = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(18)])
    categories = models.CharField(max_length=100, choices=categories)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, related_name='writers')

    class Meta:
        permissions = (("can_view_writer_list", "Can view writer list"),
                       ("can_add_writer", "Can add writer"),
                       ("can_edit_writer", "Can edit writer"),
                       ("can_delete_writer", "Can delete writer"))

    def __str__(self):
        return self.name + ' ' + self.surname

    def deactive(self, obj):
        super().deactive(obj)
        books = obj.books.filter(active=True)
        for book in books:
            super().deactive(book)
