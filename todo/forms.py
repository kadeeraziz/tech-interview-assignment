from datetime import datetime
from django.forms import ModelForm, DateTimeInput
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Task

class TaskForm(ModelForm):
    """
    A ModelForm for creating or updating a Task instance.

    The form includes fields for the Task's title, description, due date, priority,
    and category. It also includes a widget for the due date field that displays a
    date-time picker in the browser.

    Attributes:
        Meta: A class containing metadata about the form, such as the model it
            relates to, the fields it includes, and any additional options.

    Note:
        This form assumes that the `Task` model has fields named `title`,
        `description`, `due_date`, `priority`, and `category`. It also assumes
        that the `due_date` field is a DateTimeField.
    """
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'priority', 'category']
        widgets = {
            'due_date': DateTimeInput(attrs={
                'type': 'datetime-local',
                'min': datetime.now().strftime('%Y-%m-%dT%H:%M')
            })
        }


class CustomUserCreationForm(UserCreationForm):
    """
    A form for creating a new user with customized fields and removing help texts.

    This form extends the UserCreationForm provided by Django to remove help texts 
    for the 'username', 'password1' and 'password2' fields. It allows creating 
    a new user with fields 'username', 'first_name', 'last_name', 'password1' 
    and 'password2'.

    Attributes:
    -----------
    model: Model
        The User model to create a new user from.
    fields: Tuple
        A tuple of field names to be included in the form.
    """
    class Meta:
        model = User
        fields = ('username','first_name', 'last_name', 'password1', 'password2')

    def __init__(self, *args, **kwargs)->None:
        """
        Initialize the CustomUserCreationForm class instance.

        This method is called when the class instance is created and removes help texts 
        for the 'username', 'password1' and 'password2' fields of the form.

        Parameters:
        -----------
        *args: Any
            Variable length argument list.
        **kwargs: Any
            Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
