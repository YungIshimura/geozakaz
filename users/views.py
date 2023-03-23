from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, UserLoginForm


def view_index(request):
    user = request.user
    if user.is_authenticated:
        if user.is_staff:
            return redirect('zakaz:application_pages')
        else:
            return redirect('zakaz:application')
    else:
        return redirect('users:user_login')


# Create your views here.
# Авторизация пользователя
def login_user(request):
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
                return redirect('zakaz:application')
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


# Вход длә организаций
def login_company(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data.get('username_or_email')
            password = form.cleaned_data.get('password')

            # Аутентификация пользователя
            user = authenticate(request, username=username_or_email, password=password)

            if user is not None:
                if user.is_staff:
                    # Аутентификация прошла успешно
                    login(request, user)
                    return redirect('zakaz:application_pages')
                else:
                    messages.error(request, 'У Вас нет прав доступа.')
            else:
                # Аутентификация не удалась
                messages.error(request, 'Пользователь с таким именем и паролем не найден.')
    else:
        form = UserLoginForm()

    context = {
        'form': form,
        'title': 'Вход для компаний'
    }

    return render(request, 'auth/login_company.html', context)


# Регистрация пользователя
def register_user(request):
    form = UserRegistrationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(request, username=username, password=password)
        login(request, user)

        messages.success(request, 'Вы успешно зарегистрировались')
        return redirect('zakaz:application')

    context = {
        'form': form,
        'title': 'Регистрация'
    }
    return render(request, 'auth/register.html', context)


# Выход из аккаунта
def logout_account(request):
    user = request.user
    if user.is_staff:
        logout(request)
        return redirect('users:login_company')
    else:
        logout(request)
        return redirect('users:user_login')


# Пользовательское соглашение
def view_agreement(request):
    return render(request, 'user_agreement.html', {'title': 'Пользовательское соглашение'})
