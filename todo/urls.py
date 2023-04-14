from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),

    path('', views.TaskListView.as_view(), name='tasks-list'),
    path('tasks/', views.TaskListView.as_view(), name='tasks-list'),
    path('task/<slug:pk>', views.TaskDetailView.as_view(), name='task-detail'),
    path('tasks/create/', views.TaskCreateView.as_view(), name='task-create'),
    path('task/<slug:pk>/update/', views.TaskUpdateView.as_view(), name='task-update'),
    path('task/<slug:pk>/delete/', views.TaskDeleteView.as_view(), name='task-delete'),
]

