from asyncio.format_helpers import _format_callback
from tkinter.messagebox import RETRY
from django.shortcuts import render, redirect
from .models import Todo
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

# Create your views here.


class CustomLoginView(LoginView):
    template_name = 'todos/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    # Redirect success URL to todos list
    def get_success_url(self):
        return reverse_lazy('todos')


class RegisterPage(FormView):
    template_name = 'todos/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('todos')

    # Redirect user to todos list after registration
    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    # Redirect register user to todos list
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('todos')
        return super(RegisterPage, self).get(*args, **kwargs)


# By default it call template todo_list.html
class TodoList(LoginRequiredMixin, ListView):
    model = Todo
    context_object_name = 'todos'  # Replace the default context object_list
    template_name = 'todos/todos.html'  # Redirect to the mention template view

    # return context data for display the object
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # returns todos for login user
        context['todos'] = context['todos'].filter(user=self.request.user)
        # returns OPEN todos for login user
        context['count'] = context['todos'].filter(status='open').count()
        # return search text in search area / input
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['todos'] = context['todos'].filter(
                title__icontains=search_input)
          #  context['tasks'] = context['tasks'].filter(title__startswith=search_input)
        context['search_input'] = search_input
        return context


# By default it call template todo_detail.html
class TodoDetail(LoginRequiredMixin, DetailView):
    model = Todo
    context_object_name = 'todo'  # Replace the default context object_list
    template_name = 'todos/todo.html'  # Redirect to the mention template view


# By default it calls template todo_form.html
class TodoCreate(LoginRequiredMixin, CreateView):
    model = Todo
    fields = ['title', 'description', 'due_date', 'tags', 'status']
    success_url = reverse_lazy('todos')

    # Validate the todos are created by login user only
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TodoCreate, self).form_valid(form)


# By default it calls template todo_form.html
class TodoUpdate(LoginRequiredMixin, UpdateView):
    model = Todo
    fields = ['title', 'description', 'due_date', 'tags', 'status']
    success_url = reverse_lazy('todos')


# By default it calls template todo_todo_confirm_delete.html
class TodoDelete(LoginRequiredMixin, DeleteView):
    model = Todo
    context_object_name = 'todo'  # Replace the default context object_list
    success_url = reverse_lazy('todos')
