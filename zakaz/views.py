import datetime
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse
from django.core.exceptions import ValidationError

from .rosreestr2 import GetArea
from .validators import validate_number
from .forms import OrderForm, OrderFileForm, CadastralNumberForm, CreateObjectNameForm
from .models import OrderFile, Order, Region, Area as area
from django.contrib import messages
import folium
import io
import os
from docx import Document
from docx.shared import Inches
from django.http import HttpResponse
from django.conf import settings
from selenium import webdriver
from urllib.parse import quote as urlquote
from io import BytesIO
from PIL import Image

User = get_user_model()


def ajax_download_map(request):
    cadastral_number = request.POST.get('cadastral_number', None)
    response = {
            'is_valid': True
        }
    GetArea(cadastral_number)

    return JsonResponse(response)


def ajax_validate_cadastral_number(request):
    cadastral_number = request.GET.get('cadastral_number', None)
    try:
        validate_number(cadastral_number)
        response = {
            'is_valid': True
        }
    except ValidationError:
        response = {
            'is_valid': False
        }

    return JsonResponse(response)


def view_order_cadastral(request, company_slug, company_number_slug):
    context = {}
    if request.method == 'POST':
        form = CadastralNumberForm(request.POST)
        if form.is_valid():
            cadastral_numbers = request.POST.getlist('select')
            response = HttpResponseRedirect(
                reverse('zakaz:order',
                        args=[company_slug, company_number_slug]))
            response.set_cookie('cadastral_numbers', cadastral_numbers)
            return response

    else:
        form = CadastralNumberForm()

    context['form'] = form

    return render(request, 'zakaz/customer_home.html', context=context)


@login_required(login_url='users:user_login')
def view_order(request, company_slug, company_number_slug):
    coordinates = []
    context = {}

    user_company = get_object_or_404(
        User, company_number_slug=company_number_slug
    )

    cadastral_numbers = eval(request.COOKIES.get('cadastral_numbers'))
    cadastral_region = Region.objects.get(
        cadastral_region_number=cadastral_numbers[0].split(':')[0])
    cadastral_area = area.objects.get(
        cadastral_area_number=cadastral_numbers[0].split(':')[1])

    for number in cadastral_numbers:
        areas = GetArea(number)
        coordinates = areas.get_coord()
    # area_map = get_map(cadastral_numbers)

    if request.method == 'POST':
            order_form = OrderForm(request.POST)
            order_files_form = OrderFileForm(request.POST, request.FILES)
            if order_form.is_valid() and order_files_form.is_valid():
                order = order_form.save()
                order.user = user_company
                # order.map = area_map
                order.coordinates = coordinates
                order.save()
                for file in request.FILES.getlist('file'):
                    OrderFile.objects.create(order=order, file=file)
                messages.success(request, 'Ваша заявка отправлена')

                return redirect(request.path)

            else:
                messages.error(request, 'Проверьте правильность введённых данных')
    else:
        order_form = OrderForm(initial={
            'cadastral_numbers': cadastral_numbers,
            'region': cadastral_region.id,
            'area': cadastral_area.id})
        order_files_form = OrderFileForm()

    context['user_company'] = user_company
    context['order_form'] = order_form
    context['order_files_form'] = order_files_form

    return render(request, 'zakaz/order.html', context=context)


@user_passes_test(lambda u: u.is_staff, login_url='users:company_login')
def view_order_pages(request, company_number_slug):
    orders = Order.objects.filter(
        user__company_number_slug=company_number_slug
    ).select_related(
        'city', 'area', 'region', 'purpose_building', 'work_objective', 'user'
    )
    context = {
        "orders": orders,
    }

    return render(request, 'zakaz/order_pages.html', context=context)


@user_passes_test(lambda u: u.is_staff, login_url='users:company_login')
def view_change_order_status(request, order_id):
    order = get_object_or_404(Order.objects.select_related(
        'city', 'area', 'region', 'purpose_building', 'work_objective', 'user'),
        id=order_id)
    files = OrderFile.objects.select_related('order').filter(order=order.pk)
    map_html = get_map(order.cadastral_numbers, order.id)
    if request.method == 'POST':
        objectname_form = CreateObjectNameForm(request.POST, instance=order)
        if objectname_form.is_valid():
            order = objectname_form.save()
            company_number_slug = order.user.company_number_slug
            return redirect(
                reverse('zakaz:order_pages', kwargs={'company_number_slug': company_number_slug}))
    else:
        objectname_form = CreateObjectNameForm(instance=order)

    context = {
        'files': files,
        'object_name_form': objectname_form,
        'order': order,
        'map_html': map_html,
        'lengt_unit': order.get_length_unit_display()
    }

    return render(request, 'zakaz/change_order_status.html', context=context)


def get_map(number_list, order_id):
    m = folium.Map(location=[55.7558, 37.6173], zoom_start=6)
    m.get_root().html.add_child(
        folium.Element("<style>.leaflet-control-attribution.leaflet-control{display:none;}</style>"))
    all_place_lat = []
    all_place_lng = []
    for number in number_list:
        areas = GetArea(number)
        coordinates = areas.get_coord()
        if coordinates:
            for coordinate in coordinates:
                for addresses in coordinate:
                    points = []
                    for pt in addresses:
                        place_lat = pt[1]
                        place_lng = pt[0]
                        all_place_lat.append(place_lat)
                        all_place_lng.append(place_lng)
                        points.append([place_lat, place_lng])
                    folium.Polygon(points, color='red', fill=True,
                                   fill_opacity=0.2).add_to(m)

                    center_point_lng = area.center['x'],
                    center_point_lat = area.center['y'],
                    folium.Marker([center_point_lat[0], center_point_lng[0]],
                                  popup=f"Участок {number}").add_to(m)

    bounds = [[min(all_place_lat), min(all_place_lng)], [
        max(all_place_lat), max(all_place_lng)]]
    center_lat = (bounds[0][0] + bounds[1][0]) / 2
    center_lng = (bounds[0][1] + bounds[1][1]) / 2
    m.location = [center_lat, center_lng]
    m.fit_bounds(bounds)
    map_html = m._repr_html_()

    order = get_object_or_404(Order, id=order_id)
    order.map = map_html
    order.save()

    return map_html


# Выгрузка DOCX
def replace_placeholders(paragraph, placeholders):
    for placeholder, value in placeholders.items():
        if placeholder in paragraph.text:
            for run in paragraph.runs:
                if placeholder in run.text:
                    if placeholder == '_обзорная_схема':
                        run.text = ""
                        width, height = Image.open(value).size
                        run.add_picture(value, width=Inches(width / 192), height=Inches(height / 192))
                    else:
                        run.text = run.text.replace(placeholder, value)


# Замена заполнителей значениями в таблице.
def replace_placeholders_in_table(table, placeholders):
    for row in table.rows:
        for cell in row.cells:
            for paragraph in cell.paragraphs:
                replace_placeholders(paragraph, placeholders)


# Замена заполнителей значениями в футере документа.
def replace_placeholders_in_footer(document, placeholders):
    sections = document.sections
    for section in sections:
        footer = section.footer
        for paragraph in footer.paragraphs:
            replace_placeholders(paragraph, placeholders)


# Замена слов по ключам в параграфах, заголовках и таблицах
def replace_placeholders_in_document(document, placeholders):
    for paragraph in document.paragraphs:
        replace_placeholders(paragraph, placeholders)

    for table in document.tables:
        replace_placeholders_in_table(table, placeholders)

    replace_placeholders_in_footer(document, placeholders)
    return document


# Генерация нового документа
def generate_docx(document_path, placeholders):
    document = Document(document_path)
    replace_placeholders_in_document(document, placeholders)
    return document


# Скачивание DOCX
def download_docx(request, document_name, document_path, placeholders):
    document = generate_docx(document_path, placeholders)

    output = io.BytesIO()
    document.save(output)
    output.seek(0)

    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )
    response['Content-Disposition'] = f'attachment; filename="{document_name}.docx"'
    return response




# Скачиваем ШИФР-ИГИ
def download_igi_docx(request, pk):
    order = get_object_or_404(Order, pk=pk)
    department = order.region.region_department.first()
    location = f"{order.region}, {order.area}, {order.city}, {order.street}, д.{order.house_number}"
    if order.building:
        location += f" {order.building}"

    date = datetime.datetime.now()
    date_now = f"{date.strftime('%Y%m%d')}-{order.pk:03d}"

    html_map = order.map

    data_url = 'data:text/html;charset=utf-8,{}'.format(urlquote(html_map))

    driver = webdriver.Chrome()
    driver.get(data_url)
    screenshot = BytesIO(driver.get_screenshot_as_png())
    driver.quit()

    document_name = 'igi'
    document_path = os.path.join(settings.MEDIA_ROOT, f'{document_name}.docx')
    if department:
        placeholders = {
            '_шифр-иги': date_now,
            '_должность_руководителя_ведомства': department.director_position,
            '_название_ведомства': department.name,
            '_фио_руководителя_ведомства': f'{department.director_surname} {department.director_name} {department.director_patronymic}',
            '_тел_ведомства': f'{department.phone_number}',
            '_почта_ведомства': department.email,
            '_дата_текущая': date.strftime("%Y-%m-%d"),
            '_имя_руководителя_ведомства': department.director_name,
            '_название_объекта_полное': order.object_name,
            '_местоположение_объекта': location,
            '_кадастровый_номер': ', '.join(order.cadastral_number),
            '_обзорная_схема': screenshot,
            '_таблица_координат': 'координаты',
            '_шифр-тема': date_now
        }
    else:
        placeholders = {}
    return download_docx(request, document_name, document_path, placeholders)
