from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields =['title', 'priority', 'due_date', 'completed']  # created_at is automatic
