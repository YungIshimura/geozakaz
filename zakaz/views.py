from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse
from .forms import OrderForm, OrderFileForm, OrderChangeStatusForm
from .models import OrderFile, TypeWork
from django.contrib import messages
from .models import Order


@login_required(login_url='users:user_login')
def view_order(request):
    context = {}
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        order_files_form = OrderFileForm(request.POST, request.FILES)
        if order_form.is_valid() and order_files_form.is_valid():
            order = order_form.save()
            for file in request.FILES.getlist('file'):
                OrderFile.objects.create(order=order, file=file)
            messages.success(request, 'Ваша заявка отправлена')
            return HttpResponseRedirect(reverse('zakaz:order'))
    else:
        order_form = OrderForm()
        order_files_form = OrderFileForm()

    context['order_form'] = order_form
    context['order_files_form'] = order_files_form
    context['order_model'] = Order

    return render(request, 'order.html', context=context)


@user_passes_test(lambda u: u.is_staff, login_url='users:company_login')
def view_order_pages(request):
    orders = Order.objects.all()
    context = {
        "orders": orders
    }

    return render(request, 'order_pages.html', context=context)


@user_passes_test(lambda u: u.is_staff, login_url='users:company_login')
def view_change_order_status(request, pk):
    context = {}
    order = Order.objects.get(id=pk)
    file = OrderFile.objects.select_related('order').filter(order=pk)
    if request.method == 'POST':
        order_form = OrderChangeStatusForm(request.POST, instance=order)
        if order_form.is_valid():
            order = order_form.save()
            order.save()
            return HttpResponseRedirect(reverse('zakaz:order_pages'))
    else:
        order_form = OrderChangeStatusForm(instance=order)

    context['file'] = file
    context['order_form'] = order_form
    context['order'] = order
    return render(request, 'change_order_status.html', context=context)
