from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpRequest
from typing import Any

from .models import Task
from django.urls import reverse_lazy
from .forms import TaskForm, CustomUserCreationForm

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.http import Http404


class BaseView(View):
    """
    Base view class for tasks-related views.

    This class provides common functionality for views that deal with tasks,
    such as retrieving a task object from the database based on a URL parameter.

    Attributes:
        None

    Methods:
        get_object: Retrieve a task object from the database based on a URL parameter.
    """

    def get_object(self, queryset=None)->Task:
        """
        Retrieve a task object from the database based on a URL parameter.

        This method retrieves a Task object from the database based on the value of
        the 'pk' URL parameter, which is expected to be a UUID. If the Task object
        is not found in the database, a Http404 exception is raised.

        Args:
            queryset (QuerySet, optional): A QuerySet of Task objects to search for
                the specified UUID. Defaults to None.

        Returns:
            Task: A Task object with the specified UUID.

        Raises:
            Http404: If no Task object with the specified UUID is found in the database.
        """
        
        return get_object_or_404(Task, uuid=self.kwargs['pk'])
    
    def dispatch(self, request, *args, **kwargs):
        """
        Override the parent class method to catch Http404 exceptions and display a custom error page.
        """
        try:
            return super().dispatch(request, *args, **kwargs)
        except Http404:
            return render(request, 'todo/404.html', {'message': 'Page not found'}, status=404)
    
    

class TaskDetailView(BaseView, DetailView):
    """
    Display detailed information about a single task.
    """
    model = Task


class TaskListView(LoginRequiredMixin, ListView):
    """
    Display a list of tasks.

    This view displays a list of tasks. The list is paginated to display 10 tasks per page.
    If the user is not authenticated, the list is empty.

    Attributes:
        model (Task): The Task model that this view operates on.
        ordering (str): The field to order the tasks by. Defaults to '-due_date'.
        paginate_by (int): The number of tasks to display per page. Defaults to 10.

    Methods:
        get_queryset: Retrieve a QuerySet of Task objects from the database.

    """
    model = Task
    ordering = ['-due_date']
    paginate_by = 10

    def get_queryset(self)->Task:
        """
        Retrieve a QuerySet of Task objects from the database.

        This method retrieves a QuerySet of Task objects from the database, filtered to
        include only tasks that belong to the current user (if authenticated). The list
        of tasks is sorted by due date, with the most urgent tasks displayed first.

        Returns:
            QuerySet: A QuerySet of Task objects.

        """
        queryset = super().get_queryset()
        user = self.request.user
        if user.is_authenticated:
            queryset = queryset.filter(user=user)
        else:
            queryset = queryset.none()
        return queryset


class TaskCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    """
    Create a new task.

    Attributes:
        model (Task): The Task model that this view operates on.
        form_class (TaskForm): The form used to create a new task.
        success_message (str): The message to display on successful task creation.

    Methods:
        get_success_url: Get the URL to redirect to after successful form submission.
        form_valid: Handle a valid form submission.
    """

    model = Task
    form_class = TaskForm
    success_message = "Task created_at successfully"

    def get_success_url(self)->str:
        """
        Get the URL to redirect to after successful form submission.

        Returns:
            str: The URL to redirect to.
        """
        return reverse_lazy('todo:task-detail', kwargs={'pk': self.object.uuid})
    
    def form_valid(self, form:TaskForm)->HttpResponse:
        """
        Handle a valid form submission.

        This method is called when a valid form is submitted. It creates a new task
        object and sets the task's user attribute to the current user.

        Args:
            form (TaskForm): The form object containing the user's input.

        Returns:
            HttpResponse: The response object.
        """
        form.instance.user = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, BaseView, UpdateView):
    """
    TaskUpdateView allows authenticated users to update an existing task.

    Attributes:
        model (Task): The Task model that this view operates on.
        form_class (TaskForm): The form used to update a task.
        success_message (str): The message to display on successful task update.

    Methods:
        get_success_url: Get the URL to redirect to after successful form submission.

    """
    model = Task
    form_class = TaskForm
    success_message = "Task updated successfully"
    
    def get_success_url(self)->str:
        """
        Get the URL to redirect to after successful form submission.

        Returns:
            str: The URL to redirect to.

        """
        return reverse_lazy('todo:task-detail', kwargs={'pk': self.object.uuid})


class TaskDeleteView(LoginRequiredMixin, BaseView, DeleteView):
    """
    TaskDeleteView allows authenticated users to delete an existing task.

    Attributes:
        model (Task): The model class used by the view to retrieve the task object.
        success_message (str): The message to display on successful deletion of a task.
        success_url (str): The URL to redirect to on successful deletion of a task.
    """
    model = Task
    success_message = "Task deleted successfully"
    success_url = reverse_lazy('todo:tasks-list')



class RegisterView(CreateView):
    """
    A view that allows a user to register for an account.

    The user is presented with a form allowing them to enter their details,
    and upon successful submission, a new user account is created and the user
    is redirected to the login page.

    If the user is already authenticated, they will be redirected to the task
    list page instead of seeing the registration form.

    Attributes:
    - form_class (Form): The form class used for user registration.
    - success_url (str): The URL to redirect to upon successful registration.
    - template_name (str): The name of the HTML template to use for rendering
      the registration form.

    Methods:
    - dispatch(request, *args, **kwargs): Overridden method that redirects
      authenticated users to the task list page and passes all other requests
      to the default implementation.
    """
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('auth:login')
    template_name = 'registration/register.html'

    def dispatch(self, request, *args, **kwargs):
        """
        Overridden method that redirects authenticated users to the task list
        """
        if self.request.user.is_authenticated:
            return redirect('todo:tasks-list') 
        return super().dispatch(request, *args, **kwargs)
    

def complete_task(request: HttpRequest, pk: str, *args: Any, **kwargs: Any) -> HttpResponse:
    """
    This function is used to complete or uncomplete a Task object by updating the 'complete' attribute of the Task.
    
    Args:
        - request (HttpRequest): The HTTP request sent to the server.
        - pk (str): The uuid of the Task object to be updated.
        
    Returns:
        - HttpResponse: The HTTP response with a redirect to the tasks-list page.
    """

    # Retrieve the Task object using the pk
    task = get_object_or_404(Task, uuid=pk)

    # Get the 'complete' parameter from the request GET parameters
    complete = request.GET.get('complete')

    # Set the 'complete' attribute of the Task to True or False depending on the 'complete' parameter
    task.complete = True if complete == 'True' else False

    # Save the updated Task object to the database
    task.save()

    # Redirect to the tasks-list page
    return redirect('todo:tasks-list')