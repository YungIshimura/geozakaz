from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse

from .forms import OrderForm, OrderFileForm, OrderChangeStatusForm
from .models import OrderFile, TypeWork
from django.contrib import messages
from .models import Order

User = get_user_model()


@login_required(login_url='users:user_login')
def view_order(request, company_id):
    user_company = User.objects.get(id=company_id)
    context = {}
    print(request.user.pk)
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        order_files_form = OrderFileForm(request.POST, request.FILES)
        if order_form.is_valid() and order_files_form.is_valid():
            order = order_form.save(commit=False)
            order.user = user_company
            order.save()
            for file in request.FILES.getlist('file'):
                OrderFile.objects.create(order=order, file=file)
            messages.success(request, 'Ваша заявка отправлена')
            return HttpResponseRedirect(reverse('zakaz:order', args=[company_id]))
    else:
        order_form = OrderForm()
        order_files_form = OrderFileForm()

    context['user_company'] = user_company
    context['order_form'] = order_form
    context['order_files_form'] = order_files_form
    context['order_model'] = Order
    context['title'] = 'Создание заявки'

    return render(request, 'order.html', context=context)


@user_passes_test(lambda u: u.is_staff, login_url='users:company_login')
def view_order_pages(request):
    orders = Order.objects.all().filter(
        status="not processed"
    ).filter(
        user_id=request.user.pk
    )
    context = {
        "orders": orders,
        "title": "Заказы"
    }

    return render(request, 'order_pages.html', context=context)


@user_passes_test(lambda u: u.is_staff, login_url='users:company_login')
def view_change_order_status(request, pk):
    order = get_object_or_404(Order, pk=pk)
    files = OrderFile.objects.select_related('order').filter(order=pk)
    type_works = TypeWork.objects.all().filter(orders=order)
    if request.method == 'POST':
        order_form = OrderChangeStatusForm(request.POST, instance=order)
        if order_form.is_valid():
            order = order_form.save()
            order.save()
            return HttpResponseRedirect(reverse('zakaz:order_pages'))
    else:
        order_form = OrderChangeStatusForm(instance=order)

    context = {
        'files': files,
        'order_form': order_form,
        'order': order,
        'type_works': type_works
    }

    return render(request, 'change_order_status.html', context=context)
