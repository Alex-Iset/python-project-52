from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages

from task_manager.labels.models import Label
from task_manager.labels.forms import LabelForm
from task_manager.constants import SUCCESS_MESSAGES, ERROR_MESSAGES


class LabelListView(LoginRequiredMixin, ListView):
    model = Label
    template_name = 'labels/list.html'
    context_object_name = 'labels'


class LabelCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Label
    form_class = LabelForm
    template_name = 'base_create_update_form.html'
    success_url = reverse_lazy('labels_list')
    success_message = SUCCESS_MESSAGES['label']['label_created']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Создать метку'
        context['submit_button_text'] = 'Создать'
        return context


class LabelUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = 'base_create_update_form.html'
    success_url = reverse_lazy('labels_list')
    success_message = SUCCESS_MESSAGES['label']['label_updated']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Изменение метки'
        context['submit_button_text'] = 'Изменить'
        return context


class LabelDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Label
    template_name = 'labels/delete.html'
    success_url = reverse_lazy('labels_list')
    success_message = SUCCESS_MESSAGES['label']['label_deleted']
    error_message = ERROR_MESSAGES['label_using']

    def form_valid(self, form):
        status = self.get_object()
        if status.tasks.exists():
            messages.error(self.request, self.error_message)
            return redirect(self.success_url)
        return super().form_valid(form)
