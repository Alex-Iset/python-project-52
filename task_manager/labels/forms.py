from django import forms

from task_manager.labels.models import Label


class LabelForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = ['name']
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Имя',
                }
            ),
        }
