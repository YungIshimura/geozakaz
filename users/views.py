from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from urllib.parse import urlparse
from .forms import UserRegistrationForm, UserLoginForm


# Create your views here.
# Авторизация пользователя
def login_user(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email_or_phone = form.cleaned_data.get('email_or_phone')
            password = form.cleaned_data.get('password')
            company_slug = request.session.get('company_slug', None)
            company_number_slug = request.session.get('company_number_slug', None)

            # Аутентификация пользователя
            user = authenticate(request, username=email_or_phone, password=password)

            if user is not None:
                # Аутентификация прошла успешно
                login(request, user)
                return HttpResponseRedirect(reverse('zakaz:cadastral', args=[company_slug, company_number_slug]))
            else:
                # Аутентификация не удалась
                messages.error(request, 'Пользователь с таким именем и паролем не найден.')
    else:
        form = UserLoginForm()

        previous_url = request.META.get('HTTP_REFERER')
        path_parts = urlparse(previous_url).path.split('/')
        company_slug = path_parts[2]
        company_number_slug = path_parts[3]
        request.session['company_slug'] = company_slug
        request.session['company_number_slug'] = company_number_slug

    context = {
        'form': form
    }

    return render(request, 'auth/login.html', context)


# Вход длә организаций
def login_company(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email_or_phone = form.cleaned_data.get('email_or_phone')
            password = form.cleaned_data.get('password')

            # Аутентификация пользователя
            user = authenticate(request, username=email_or_phone, password=password)

            if user is not None:
                if user.is_staff:
                    # Аутентификация прошла успешно
                    login(request, user)
                    company_number_slug = user.company_number_slug
                    return redirect(reverse('zakaz:order_pages', kwargs={'company_number_slug': company_number_slug}))
                else:
                    messages.error(request, 'У Вас нет прав доступа.')
            else:
                # Аутентификация не удалась
                messages.error(request, 'Пользователь с таким именем и паролем не найден.')
    else:
        form = UserLoginForm()

    context = {
        'form': form
    }

    return render(request, 'auth/login_company.html', context)


# Регистрация пользователя
def register_user(request):
    form = UserRegistrationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password1')
        user = authenticate(request, email=email, password=password)
        login(request, user)

        messages.success(request, 'Вы успешно зарегистрировались')

        company_slug = request.session.get('company_slug', None)
        company_number_slug = request.session.get('company_number_slug', None)
        return HttpResponseRedirect(reverse('zakaz:cadastral', args=[company_slug, company_number_slug]))

    previous_url = request.META.get('HTTP_REFERER')
    path_parts = urlparse(previous_url).path.split('/')
    company_slug = path_parts[2]
    company_number_slug = path_parts[3]
    request.session['company_slug'] = company_slug
    request.session['company_number_slug'] = company_number_slug

    context = {
        'form': form
    }
    return render(request, 'auth/register.html', context)


# Выход из аккаунта
def logout_account(request):
    user = request.user
    if user.is_staff:
        logout(request)
        return redirect('users:company_login')
    else:
        logout(request)
        return redirect('users:user_login')


# Пользовательское соглашение
def view_agreement(request):
    return render(request, 'users/user_agreement.html')
