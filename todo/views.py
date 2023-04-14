from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
import uuid
from django.shortcuts import get_object_or_404


from django.shortcuts import render
from django.http import HttpResponse

from .models import Task, Category
from django.urls import reverse_lazy
from .forms import TaskForm

from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import UserCreationForm



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



class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm


    def get_success_url(self):
        return reverse_lazy('todo:task-detail', kwargs={'pk': self.object.uuid})
    



class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm

    def get_object(self, queryset=None):
        id = uuid.UUID(self.kwargs['pk'])
        obj = get_object_or_404(Task, uuid=id)
        return obj
    
    def get_success_url(self):
        return reverse_lazy('todo:task-detail', kwargs={'pk': self.object.uuid})
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    

class TaskDeleteView(DeleteView):
    model = Task
    success_url = '/tasks/'

    def get_object(self, queryset=None):
        id = uuid.UUID(self.kwargs['pk'])
        obj = get_object_or_404(Task, uuid=id)
        return obj
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    
class LoginView(LoginView):
    template_name = 'login.html'
    success_url = reverse_lazy('todo:tasks-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        return HttpResponseRedirect(self.get_success_url())


class LogoutView(LogoutView):
    template_name = 'logout.html'
    success_url = reverse_lazy('todo:tasks-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        return HttpResponseRedirect(self.get_success_url())
    

class RegisterView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('todo:login')
    template_name = 'register.html'
    



