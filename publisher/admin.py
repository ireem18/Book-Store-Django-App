from django.contrib import admin
from .models import Publisher

class PublisherAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "started_date")

admin.site.register(Publisher, PublisherAdmin)
