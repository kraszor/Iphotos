from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError


def validate_email(value):
    if User.objects.filter(email = value).exists():
        raise ValidationError(f"{value} is already taken.", params={'value': value})


class RegisterUserForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}), validators=[validate_email])
    first_name = forms.CharField(max_length=50, label="First name",
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=50, label="Last name",
                                widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = "Username"
        self.fields['first_name'].widget.attrs['placeholder'] = "First name"
        self.fields['last_name'].widget.attrs['placeholder'] = "Last name"
        self.fields['email'].widget.attrs['placeholder'] = "Email"
        self.fields['password1'].widget.attrs['placeholder'] = "Password"
        self.fields['password2'].widget.attrs['placeholder'] = "Confirm password"


class EditProfileForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
        )

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'


class FormChangePassword(PasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super(FormChangePassword, self).__init__(*args, **kwargs)
        for field in ('old_password', 'new_password1', 'new_password2'):
            self.fields[field].widget.attrs = {'class': 'form-control'}