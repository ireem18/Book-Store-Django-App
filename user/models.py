from django.db import models


class BaseModel(models.Model):
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True

    def deactive(self):
        self.active = False
        self.save()
