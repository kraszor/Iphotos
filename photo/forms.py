from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from .models import UsersGroup


class CreateGroupForm(forms.ModelForm):
    class Meta:
        model = UsersGroup
        fields = ['name', 'description', 'users']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name of the group'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description of the group'}),
            'users': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

        # def __init__(self, *args, **kwargs):
        #     self.fields['users'] = forms.ModelMultipleChoiceField(queryset=User.objects.get.all().exclude(username='kraszor'), widget=forms.SelectMultiple(attrs={'class': 'form-control'}))