from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.constants import ERROR_MESSAGES, SUCCESS_MESSAGES
from task_manager.statuses.forms import StatusForm
from task_manager.statuses.models import Status


class StatusListView(LoginRequiredMixin, ListView):
    model = Status
    template_name = 'statuses/list.html'
    context_object_name = 'statuses'


class StatusCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Status
    form_class = StatusForm
    template_name = 'base_create_update_form.html'
    success_url = reverse_lazy('statuses_list')
    success_message = SUCCESS_MESSAGES['status']['status_created']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Создать статус'
        context['submit_button_text'] = 'Создать'
        return context


class StatusUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'base_create_update_form.html'
    success_url = reverse_lazy('statuses_list')
    success_message = SUCCESS_MESSAGES['status']['status_updated']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Изменение статуса'
        context['submit_button_text'] = 'Изменить'
        return context


class StatusDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Status
    template_name = 'statuses/delete.html'
    success_url = reverse_lazy('statuses_list')
    success_message = SUCCESS_MESSAGES['status']['status_deleted']
    error_message = ERROR_MESSAGES['status_using']

    def form_valid(self, form):
        status = self.get_object()
        if status.tasks.exists():
            messages.error(self.request, self.error_message)
            return redirect(self.success_url)
        return super().form_valid(form)
