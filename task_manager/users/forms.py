from django import forms
from django.contrib.auth.forms import UserCreationForm

from task_manager.users.models import User
from task_manager.constants import USER_FIELD_TEXTS


class BaseUserFormMixin:
    def __init__(self, field_texts=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        field_texts = field_texts or USER_FIELD_TEXTS

        for field_name, field in self.fields.items():
            field_config = field_texts.get(field_name, {})

            field.label_suffix = ''

            field.label = field_config.get('label', field.label)
            field.help_text = field_config.get('help_text', field.help_text)
            placeholder = field_config.get('placeholder')

            if placeholder:
                field.widget.attrs['placeholder'] = placeholder

            field.widget.attrs.setdefault('class', 'form-control')


class UserCreateForm(BaseUserFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password1', 'password2']


class UserUpdateForm(BaseUserFormMixin, forms.ModelForm):
    password1 = forms.CharField()
    password2 = forms.CharField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password1', 'password2']
