from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse

from .forms import OrderForm, OrderFileForm, OrderChangeStatusForm
from .models import OrderFile, TypeWork, Order
from django.contrib import messages
from django.utils.crypto import get_random_string
from rosreestr2coord import Area
import folium

User = get_user_model()


# @login_required(login_url='users:user_login')
def view_order(request, company_id):
    user_company = get_object_or_404(User, id=company_id)
    context = {}
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        order_files_form = OrderFileForm(request.POST, request.FILES)
        if order_form.is_valid() and order_files_form.is_valid():
            order = order_form.save()
            order.user = user_company
            order.slug = get_random_string(6, '0123456789')
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
        user_id=request.user.pk
    )
    context = {
        "orders": orders,
    }

    return render(request, 'order_pages.html', context=context)


@user_passes_test(lambda u: u.is_staff, login_url='users:company_login')
def view_change_order_status(request, slug):
    order = get_object_or_404(Order, slug=slug)
    files = OrderFile.objects.select_related('order').filter(order=order.pk)
    type_works = TypeWork.objects.all().filter(orders=order)
    map_html = get_map(order.cadastral_number)
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
        'type_works': type_works,
        'map_html': map_html
    }

    return render(request, 'change_order_status.html', context=context)


def get_map(number):
    points = []
    area = Area(number, with_proxy=False)
    coordinates = area.get_coord()
    for coordinate in coordinates:
        for addresses in coordinate:
            m = folium.Map((addresses[0][1], addresses[0][0]), zoom_start=16)
            for pt in addresses:
                place_lat = [pt[1] for pt in addresses]
                place_lng = [pt[0] for pt in addresses]

                for i in range(len(place_lat)):
                    points.append([place_lat[i], place_lng[i]])
                folium.PolyLine(points, color='red').add_to(m)

    folium.PolyLine(points, color='red').add_to(m)
    map_html = m._repr_html_()
    return map_html
