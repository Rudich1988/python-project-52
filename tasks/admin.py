from django.contrib import admin

from tasks.models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'author',
                    'status', 'executor', 'created_at']
    search_fields = ['name', 'author']
