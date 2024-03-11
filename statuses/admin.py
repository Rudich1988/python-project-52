from django.contrib import admin
from .models import Status


@admin.register(Status)
class UserAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
