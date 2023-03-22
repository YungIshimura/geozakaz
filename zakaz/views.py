from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse
from .forms import OrderForm, OrderFileForm
from .models import OrderFile
from .models import Order, TypeWork, Region, Area


def view_order(request):
    context = {}
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        order_files_form = OrderFileForm(request.POST, request.FILES)
        if order_form.is_valid() and order_files_form.is_valid():
            order = order_form.save()
            for file in request.FILES.getlist('file'):
                order_file = OrderFile.objects.create(order=order, file=file)
                print(order_file)

            return HttpResponseRedirect(reverse('zakaz:order_pages'))

    else:
        order_form = OrderForm()
        order_files_form = OrderFileForm()

    context['order_form'] = order_form
    context['order_files_form'] = order_files_form

    return render(request, 'order.html', context=context)


def view_order_pages(request):
    orders = Order.objects.all()
    context = {
        "orders": orders,
    }

    return render(request, 'order_pages.html', context=context)


def change_order_status_view(request, pk):
    order = Order.objects.get(id=pk)
    print(order)
    return render(request, 'order.html')
