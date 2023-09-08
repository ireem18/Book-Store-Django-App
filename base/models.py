from abc import abstractmethod

from django.db import models


class ActiveManager(models.Manager):
    def active(self):
        return self.model.objects.filter(active=True)


class BaseModel(models.Model):
    active = models.BooleanField(default=True)
    objects = ActiveManager()

    class Meta:
        abstract = True

    def deactive(self, obj):
        obj.active = False
        obj.save()
