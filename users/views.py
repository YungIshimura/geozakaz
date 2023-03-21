from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, UserLoginForm


# Create your views here.
def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data.get('username_or_email')
            password = form.cleaned_data.get('password')

            # Аутентификация пользователя
            user = authenticate(request, username=username_or_email, password=password)

            if user is not None:
                # Аутентификация прошла успешно
                login(request, user)
                return redirect('users:user_register')
            else:
                # Аутентификация не удалась
                messages.error(request, 'Пользователь с таким именем и паролем не найден.')
    else:
        form = UserLoginForm()

    context = {
        'form': form,
        'title': 'Авторизация'
    }

    return render(request, 'auth/login.html', context)


def user_register(request):
    form = UserRegistrationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Вы успешно зарегистрировались')
        return redirect('users:user_login')

    context = {
        'form': form,
        'title': 'Регистрация'
    }
    return render(request, 'auth/register.html', context)


def user_logout(request):
    logout(request)
    return redirect('users:user_login')
