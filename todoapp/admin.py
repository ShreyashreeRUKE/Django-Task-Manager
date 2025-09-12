from django.contrib import admin
from .models import Task as Todo

class TodoAdmin(admin.ModelAdmin):
    list_display = ('title', 'completed', 'created_at')
    list_filter = ('completed', 'created_at')

admin.site.register(Todo, TodoAdmin)
