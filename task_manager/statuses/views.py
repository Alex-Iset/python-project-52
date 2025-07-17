from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages

from task_manager.statuses.models import Status
from task_manager.statuses.forms import StatusForm
from task_manager.constants import SUCCESS_MESSAGES, ERROR_MESSAGES


class StatusListView(LoginRequiredMixin, ListView):
    model = Status
    template_name = 'statuses/list.html'
    context_object_name = 'statuses'


class StatusCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/form.html'
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
    template_name = 'statuses/form.html'
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

    def delete(self, request, *args, **kwargs):
        status = self.get_object()
        if status.task_set.exists():
            messages.error(request, self.error_message)
            return self.render_to_response(self.get_context_data())

        return super().delete(request, *args, **kwargs)
