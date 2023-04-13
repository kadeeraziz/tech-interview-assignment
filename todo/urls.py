from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('tasks/', views.TaskListView.as_view(), name='tasks-list'),
    path('task/<slug:pk>', views.TaskDetailView.as_view(), name='task-detail'),
    path('tasks/create/', views.TaskCreateView.as_view(), name='task-create'),
    path('task/<slug:pk>/update/', views.TaskUpdateView.as_view(), name='task-update'),
    path('task/<slug:pk>/delete/', views.TaskDeleteView.as_view(), name='task-delete'),
]

