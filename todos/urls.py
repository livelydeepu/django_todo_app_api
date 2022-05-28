from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.RegisterPage.as_view(), name='register'),
    path('', views.TodoList.as_view(), name='todos'),
    path('todo/<int:pk>/', views.TodoDetail.as_view(), name='todo'),
    path('todo-create/', views.TodoCreate.as_view(), name='todo-create'),
    path('todo-update/<int:pk>/', views.TodoUpdate.as_view(), name='todo-update'),
    path('todo-delete/<int:pk>/', views.TodoDelete.as_view(), name='todo-delete'),
]
