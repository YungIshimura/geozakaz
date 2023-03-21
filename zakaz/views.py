from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse
from .forms import OrderForm, OrderFileForm


def view_application(request):
    context = {}
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        order_files_form = OrderFileForm(request.POST, request.FILES)
        if order_form.is_valid() and order_files_form.is_valid():
            order=order_form.save()
            order_files = order_files_form.save(commit=False)
            order_files.order = order
            order_files.save()

            return HttpResponseRedirect(reverse('zakaz:application_pages'))
        else:
            print(order_form.errors)
            print(order_files_form.errors)
    else:
        order_form = OrderForm()
        order_files_form = OrderFileForm()

    context['order_form'] = order_form
    context['order_files_form'] = order_files_form

    return render(request, 'application.html', context=context)


def view_application_pages(request):
    return render(request, 'application_pages.html')
