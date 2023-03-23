from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse
from .forms import OrderForm, OrderFileForm
from .models import OrderFile
from django.contrib import messages


@login_required(login_url='users:user_login')
def view_application(request):
    context = {}
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        order_files_form = OrderFileForm(request.POST, request.FILES)
        if order_form.is_valid() and order_files_form.is_valid():
            order = order_form.save()
            for file in request.FILES.getlist('file'):
                order_file = OrderFile.objects.create(order=order, file=file)
                print(order_file)

            return HttpResponseRedirect(reverse('zakaz:application_pages'))
        else:
            messages.error(request, 'Проверьте правильность введённый данных')

    else:
        order_form = OrderForm()
        order_files_form = OrderFileForm()

    context['order_form'] = order_form
    context['order_files_form'] = order_files_form

    return render(request, 'application.html', context=context)


@user_passes_test(lambda u: u.is_staff, login_url='users:company_login')
def view_application_pages(request):
    return render(request, 'application_pages.html')
