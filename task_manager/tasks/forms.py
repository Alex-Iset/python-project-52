from django import forms

from task_manager.users.models import User
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.labels.models import Label
from task_manager.constants import TASK_FIELD_TEXTS


class BaseTaskFormMixin:
    def __init__(self, field_texts=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        field_texts = field_texts or TASK_FIELD_TEXTS

        for field_name, field in self.fields.items():
            field_config = field_texts.get(field_name, {})

            field.label = field_config.get('label', field.label)
            placeholder = field_config.get('placeholder')

            if placeholder:
                field.widget.attrs['placeholder'] = placeholder

            if field.widget.__class__.__name__ == 'Select':
                field.widget.attrs.setdefault('class', 'form-select')
            field.widget.attrs.setdefault('class', 'form-control')


class TaskForm(BaseTaskFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].queryset = Status.objects.all()
        self.fields['executor'].queryset = User.objects.all()
        self.fields['labels'].queryset = Label.objects.all()

    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']
