from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
import uuid
from django.shortcuts import get_object_or_404
from django import forms

from django.shortcuts import render
from django.http import HttpResponse

from .models import Task, Category
from django.urls import reverse_lazy



class TaskListView(ListView):
    model = Task
    template_name = 'todo/task_list.html'
    context_object_name = 'tasks'
    ordering = ['-created']
    paginate_by = 10


class TaskDetailView(DetailView):
    model = Task
    template_name = 'todo/task_detail.html'
    context_object_name = 'task'

    def get_object(self, queryset=None):
        id = uuid.UUID(self.kwargs['pk'])
        obj = get_object_or_404(Task, uuid=id)
        return obj


class TaskCreateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due', 'priority', 'category']
        widgets = {
            'due': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }

class TaskCreateView(CreateView):
    model = Task
    form_class = TaskCreateForm


    def get_success_url(self):
        return reverse_lazy('todo:task-detail', kwargs={'pk': self.object.uuid})



class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskCreateForm

    def get_object(self, queryset=None):
        id = uuid.UUID(self.kwargs['pk'])
        obj = get_object_or_404(Task, uuid=id)
        return obj
    
    def get_success_url(self):
        return reverse_lazy('todo:task-detail', kwargs={'pk': self.object.uuid})
    

class TaskDeleteView(DeleteView):
    model = Task
    success_url = '/tasks/'

    def get_object(self, queryset=None):
        id = uuid.UUID(self.kwargs['pk'])
        obj = get_object_or_404(Task, uuid=id)
        return obj

    
# Create your views here.
def index(request):
    return render(request, 'index.html')



