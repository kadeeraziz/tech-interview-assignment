from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
import uuid
from django.shortcuts import get_object_or_404


from django.shortcuts import render
from django.http import HttpResponse

from .models import Task, Category
from django.urls import reverse_lazy
from .forms import TaskForm

from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import UserCreationForm



class TaskListView(ListView):
    model = Task
    ordering = ['-created']
    paginate_by = 10


class TaskDetailView(DetailView):
    model = Task

    def get_object(self, queryset=None):
        return get_object_or_404(Task, uuid=self.kwargs['pk'])



class TaskCreateView(SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskForm
    success_message = "Task created successfully"

    def get_success_url(self):
        return reverse_lazy('todo:task-detail', kwargs={'pk': self.object.uuid})
    


@method_decorator(login_required, name='dispatch')
class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm

    def get_object(self, queryset=None):
        return get_object_or_404(Task, uuid=self.kwargs['pk'])
    
    def get_success_url(self):
        return reverse_lazy('todo:task-detail', kwargs={'pk': self.object.uuid})


@method_decorator(login_required, name='dispatch')
class TaskDeleteView(DeleteView):
    model = Task
    success_url = reverse_lazy('todo:tasks-list')

    def get_object(self, queryset=None):
        return get_object_or_404(Task, uuid=self.kwargs['pk'])
    
    
class LoginView(LoginView, SuccessMessageMixin):
    template_name = 'registration/login.html'
    success_url = reverse_lazy('todo:tasks-list')
    success_message = "Logged in successfully"



class LogoutView(SuccessMessageMixin, LogoutView):
    template_name = 'todo/task_list.html'
    success_url = reverse_lazy('todo:tasks-list')
    success_message = "Logged out successfully"
    

class RegisterView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('todo:login')
    template_name = 'registration/register.html'
    



