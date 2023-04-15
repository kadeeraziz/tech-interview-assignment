from datetime import datetime
from django.forms import ModelForm, DateTimeInput
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Task

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due', 'priority', 'category']
        widgets = {
            'due': DateTimeInput(attrs={
                'type': 'datetime-local',
                'min': datetime.now().strftime('%Y-%m-%dT%H:%M')
            })
        }


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
