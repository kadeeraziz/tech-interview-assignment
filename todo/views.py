from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404

from .models import Task, Category
from django.urls import reverse_lazy
from .forms import TaskForm

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect


class BaseView(View):
    def get_object(self, queryset=None):
        return get_object_or_404(Task, uuid=self.kwargs['pk'])
    

class TaskDetailView(BaseView, DetailView):
    model = Task


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    ordering = ['-created']
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if user.is_authenticated:
            queryset = queryset.filter(user=user)
        else:
            queryset = queryset.none()
        return queryset


class TaskCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    success_message = "Task created successfully"

    def get_success_url(self):
        return reverse_lazy('todo:task-detail', kwargs={'pk': self.object.uuid})
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, BaseView, UpdateView):
    model = Task
    form_class = TaskForm
    success_message = "Task updated successfully"
    
    def get_success_url(self):
        return reverse_lazy('todo:task-detail', kwargs={'pk': self.object.uuid})


class TaskDeleteView(LoginRequiredMixin, BaseView, DeleteView):
    model = Task
    success_url = reverse_lazy('todo:tasks-list')



def complete_task(request, pk, *args, **kwargs):
    task = get_object_or_404(Task, uuid=pk)
    complete = request.GET.get('complete')
    task.complete = True if complete == 'True' else False
    task.save()
    return redirect('todo:tasks-list')



class RegisterView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('auth:login')
    template_name = 'registration/register.html'
    



