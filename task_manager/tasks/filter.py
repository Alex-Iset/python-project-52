import django_filters
from django import forms

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.users.models import User


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(
        queryset=Status.objects.all(),
        label='Статус',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    executor = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        label='Исполнитель',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    labels = django_filters.ModelChoiceFilter(
        queryset=Label.objects.all(),
        label='Метки',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    self_tasks = django_filters.BooleanFilter(
        label='Только свои задачи',
        method='filter_self_tasks',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels', 'self_tasks']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for filter_obj in self.filters.values():
            self.apply_widget_classes(filter_obj)

    def apply_widget_classes(self, filter_obj):
        widget = getattr(filter_obj, 'widget', None)
        if not widget:
            return

        if not hasattr(widget, 'attrs'):
            widget.attrs = {}

        if isinstance(widget, forms.CheckboxInput):
            widget.attrs.setdefault('class', 'form-check-input')
        elif isinstance(widget, (forms.Select, forms.SelectMultiple)):
            widget.attrs.setdefault('class', 'form-select')
        else:
            widget.attrs.setdefault('class', 'form-control')

    def filter_self_tasks(self, queryset, _name, value):
        if value and self.request and self.request.user.is_authenticated:
            return queryset.filter(author=self.request.user)
        return queryset.all()
