from django.urls import path
from .views import (
    TaskListView,
    TaskDetailView,
    TaskCreateView,
    TaskUpdateView, 
    TaskDeleteView,
)
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', TaskListView.as_view(), name='tasks-list'),
    path('tasks/', TaskListView.as_view(), name='tasks-list'),
    path('task/<slug:pk>', TaskDetailView.as_view(), name='task-detail'),
    path('tasks/create/', TaskCreateView.as_view(), name='task-create'),
    path('task/<slug:pk>/update/', TaskUpdateView.as_view(), name='task-update'),
    path('task/<slug:pk>/delete/', TaskDeleteView.as_view(), name='task-delete'),

]

