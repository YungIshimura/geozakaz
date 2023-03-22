from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from .models import User
from phonenumber_field.formfields import PhoneNumberField


# Форма регистрации пользователя
class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'patronymic', 'email', 'phone', 'username', 'password1', 'password2',
            'agreement'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field != 'agreement':
                self.fields[field].widget.attrs.update({'class': 'form-control'})
        self.fields['phone'].widget.attrs.update({
            'region': 'RU',
            'error_messages': {
                'invalid': _(
                    'Введите действительный номер телефона (например, 8 (301) 123-45-67) '
                    'или номер с префиксом международного вызова'),
            }
        })

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(_('Этот email уже используется.'))
        return email


# Форма авторизации пользователя
class UserLoginForm(forms.Form):
    username_or_email = forms.CharField(label='Логин или email',
                                        widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
