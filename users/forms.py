from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _
from .models import User
from phonenumber_field.formfields import PhoneNumberField


# Форма регистрации пользователя
class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            'email', 'phone_number', 'password1', 'password2',
            'agreement'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field != 'agreement':
                self.fields[field].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'autofocus': False})
        self.fields['phone_number'].widget.attrs.update({
            'region': 'RU',
            'error_messages': {
                'invalid': _(
                    'Введите действительный номер телефона (например, 8 (301) 123-45-67) '
                    'или номер с префиксом международного вызова'),
            }
        })

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not phone_number:
            raise forms.ValidationError('Это обязательное поле')
        return phone_number

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError('Это обязательное поле')
        try:
            validate_email(email)
        except forms.ValidationError:
            raise forms.ValidationError('Введите действительный адрес электронной почты')
        return email
    # def clean_email(self):
    #     email = self.cleaned_data['email']
    #     if User.objects.filter(email=email).exists():
    #         raise forms.ValidationError(_('Этот email уже используется.'))
    #     return email


# Форма авторизации пользователя
class UserLoginForm(forms.Form):
    email_or_phone = forms.CharField(label='Email или номер телефона',
                                     widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
