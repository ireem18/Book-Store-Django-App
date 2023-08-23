from django.contrib import admin
from .models import Writer
class WriterAdmin(admin.ModelAdmin):
    list_display = ("name", "surname", "publisher")

admin.site.register(Writer, WriterAdmin)
