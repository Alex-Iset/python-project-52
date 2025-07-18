from django_filters.views import FilterView
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy

from task_manager.tasks.models import Task
from task_manager.tasks.forms import TaskForm
from task_manager.tasks.filter import TaskFilter
from task_manager.constants import SUCCESS_MESSAGES, ERROR_MESSAGES


class TaskListView(LoginRequiredMixin, FilterView):
    model = Task
    filterset_class = TaskFilter
    template_name = 'tasks/list.html'
    context_object_name = 'tasks'


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/detail.html'
    context_object_name = 'task'


class TaskCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/form.html'
    success_url = reverse_lazy('tasks_list')
    success_message = SUCCESS_MESSAGES['task']['task_created']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Создать задачу'
        context['submit_button_text'] = 'Создать'
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/form.html'
    success_url = reverse_lazy('tasks_list')
    success_message = SUCCESS_MESSAGES['task']['task_updated']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Изменение задачи'
        context['submit_button_text'] = 'Изменить'
        return context


class TaskDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Task
    template_name = 'tasks/delete.html'
    success_url = reverse_lazy('tasks_list')
    success_message = SUCCESS_MESSAGES['task']['task_deleted']
    error_message = ERROR_MESSAGES['only_author_can_delete']

    def get(self, request, *args, **kwargs):
        task = self.get_object()
        if task.author != request.user and not request.user.is_superuser:
            messages.error(request, self.error_message)
            return redirect(self.success_url)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        task = self.get_object()
        if task.author != request.user and not request.user.is_superuser:
            messages.error(request, self.error_message)
            return redirect(self.success_url)
        return super().post(request, *args, **kwargs)
