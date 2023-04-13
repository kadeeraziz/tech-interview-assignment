
from django.db.models import (
    Model,
    UUIDField,
    CharField,
    DateTimeField,
    TextField,
    BooleanField,
    ForeignKey,
    CASCADE,
    Index
)

from uuid import uuid4



PRIORITY_CHOICES = (
    ('low', 'Low'),
    ('medium', 'Medium'),
    ('high', 'High'),
)

class BaseModel(Model):
    uuid = UUIDField(
        default=uuid4, editable=False,
        unique=True, db_index=True)
    created = DateTimeField(auto_now_add=True)
    modified = DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Category(BaseModel):
    name = CharField(max_length=200)

    def __str__(self):
        return self.name

class Task(BaseModel):
    title = CharField(max_length=200)
    description = TextField(null=True, blank=True)
    complete = BooleanField(default=False)
    due = DateTimeField(null=True, blank=True)
    priority = CharField(max_length=10, choices=PRIORITY_CHOICES, default='low')
    category = ForeignKey(Category, on_delete=CASCADE, default=None)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['complete'] 
        indexes = [Index(fields=['title'])]

