from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from .models import User


# Форма создания пользователя
class UserRegistrationForm(UserCreationForm):
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Подтвердите пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={'class': 'form-control'}))
    patronymic = forms.CharField(label='Отчество', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(label='Телефон', widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'patronymic', 'email', 'phone', 'username', 'password1', 'password2')

    # проверка свободен ли email
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(_('Этот email уже используется.'))
        return email


# Форма регистрации пользователя
class UserLoginForm(forms.Form):
    username_or_email = forms.CharField(label='Логин или email',
                                        widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
