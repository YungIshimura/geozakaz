import datetime
import json
import random
import time

import openpyxl as openpyxl
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
from .models import OrderFile, Order, Region, Area as area, TypeWork
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
            cadastral_numbers = request.POST.getlist('cadastral_numbers')
            response = HttpResponseRedirect(
                reverse('zakaz:order',
                        args=[company_slug, company_number_slug]))
            response.set_cookie('cadastral_numbers', cadastral_numbers)
            return response

    else:
        form = CadastralNumberForm()

    context['form'] = form

    return render(request, 'zakaz/customer_home.html', context=context)


# @login_required(login_url='users:user_login')
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
        coordinates += areas.get_coord()

    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        order_files_form = OrderFileForm(request.POST, request.FILES)
        if order_form.is_valid() and order_files_form.is_valid():
            order = order_form.save()
            order.user = user_company
            order.coordinates = coordinates
            order.map = get_map(order.cadastral_numbers)

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
    type_work = TypeWork.objects.all().filter(orders=order.pk)
    files = OrderFile.objects.select_related('order').filter(order=order.pk)
    map_html = get_map(order.cadastral_numbers)
    if request.method == 'POST':
        objectname_form = OrderForm(request.POST, instance=order)
        if objectname_form.is_valid():
            order = objectname_form.save()
            company_number_slug = order.user.company_number_slug
            return redirect(
                reverse('zakaz:change_order_status', kwargs={'order_id': order_id}))
    else:
        objectname_form = OrderForm(instance=order)

    context = {
        'type_works': type_work,
        'files': files,
        'order_form': objectname_form,
        'order': order,
        'map_html': map_html,
        'lengt_unit': order.get_length_unit_display()
    }

    return render(request, 'zakaz/change_order_status.html', context=context)


def get_map(number_list):
    m = folium.Map(location=[55.7558, 37.6173], zoom_start=6, zoom_control=False,
                   control_scale=True,
                   )

    m.options.update({'max_width': '100%'})
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
                    folium.Polygon(points, color='red').add_to(m)

                    center_point_lng = areas.center['x'],
                    center_point_lat = areas.center['y'],
                    folium.CircleMarker(
                        location=[center_point_lat[0], center_point_lng[0]],
                        popup=folium.Popup(f':{number.split(":")[-1]}', show=True),
                        opacity=0,
                    ).add_to(m)

    m.get_root().html.add_child(
        folium.Element("<style>.leaflet-popup-close-button {display: none;}</style>"))
    bounds = [[min(all_place_lat), min(all_place_lng)], [
        max(all_place_lat), max(all_place_lng)]]
    center_lat = (bounds[0][0] + bounds[1][0]) / 2
    center_lng = (bounds[0][1] + bounds[1][1]) / 2
    m.location = [center_lat, center_lng]
    m.fit_bounds(bounds)
    map_html = m._repr_html_()

    # order = get_object_or_404(Order, id=order_id)
    # order.map = map_html
    # order.save()

    return map_html


# Выгрузка DOCX
# Замена заполнителей значениями в абзаце.
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


# Замена заполнителей значениями во всех абзацах и таблицах документа
def replace_placeholders_in_document(document, placeholders):
    for paragraph in document.paragraphs:
        replace_placeholders(paragraph, placeholders)

    for table in document.tables:
        replace_placeholders_in_table(table, placeholders)

    replace_placeholders_in_footer(document, placeholders)

    return document


# Генерация нового документа с заменой заполнителей значениями.
def generate_docx(document_path, placeholders):
    document = Document(document_path)
    replace_placeholders_in_document(document, placeholders)
    return document


def add_table(document):
    for paragraph in document.paragraphs:
        if '_таблица_координат' in paragraph.text:
            # Добавляем пустую таблицу 2 на 3.
            table = document.add_table(rows=2, cols=3)
            # Добавляем ячейки в таблицу.
            for row in table.rows:
                for cell in row.cells:
                    cell.text = ''
            # Вставляем таблицу после абзаца, содержащего "_таблица координат".
            paragraph.insert_paragraph_before('Table Grid', style='Normal')
            break



# Скачивание DOCX
def download_docx(request, document_name, document_path, document_cipher, placeholders):
    document = generate_docx(document_path, placeholders)

    add_table(document)

    output = io.BytesIO()
    document.save(output)
    output.seek(0)

    document_name_upload = f'{document_cipher}-{document_name}'

    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )
    response['Content-Disposition'] = f'attachment; filename="{document_name_upload}.docx"'
    return response


# Скачиваем ШИФР-ИГИ
def download_igi_docx(request, pk):
    order = get_object_or_404(Order, pk=pk)
    department = order.region.region_department.first()
    location = f"{order.region}, {order.area}, {order.city}, {order.street}, д.{order.house_number}"
    if order.building:
        location += f" {order.building}"

    date = datetime.datetime.now()
    document_cipher = f"{date.strftime('%Y%m%d')}-{order.pk:03d}"

    cadastral_numbers = order.cadastral_numbers
    coordinates = json.loads(order.coordinates)

    coordinates_dict = {}

    for i, coords in enumerate(coordinates):
        cadastral_num = cadastral_numbers[i]
        coordinates_dict[cadastral_num] = coords[0]

    print(coordinates_dict)

    # data = []
    # for i, number in enumerate(cadastral_numbers):
    #     data.append(f"{number}: {coordinates[i][0]}")
    #
    # formatted_data = '\n'.join(data)
    data = ""
    for key, value in coordinates_dict.items():
        data += f"\nКоординаты углов участка {key}\n"
        data += "Номер точки\tКоордината Х\tКоордината У\n"
        for i, point in enumerate(value):
            data += f"{i + 1}\t\t{point[0]}\t\t{point[1]}\n"

    document_name = 'IGI'
    document_path = os.path.join(settings.MEDIA_ROOT, f'{document_name}.docx')

    if department:
        placeholders = {
            '_шифр-иги': document_cipher,
            '_должность_руководителя_ведомства': department.director_position,
            '_название_ведомства': department.name,
            '_фио_руководителя_ведомства': f'{department.director_surname} {department.director_name} {department.director_patronymic}',
            '_тел_ведомства': str(department.phone_number),
            '_почта_ведомства': department.email,
            '_дата_текущая': date.strftime("%Y-%m-%d"),
            '_имя_руководителя_ведомства': department.director_name,
            '_название_объекта_полное': order.object_name,
            '_местоположение_объекта': location,
            '_кадастровый_номер': ', '.join(cadastral_numbers),
            # '_таблица_координат': data,
            '_шифр-тема': document_cipher
        }
    else:
        placeholders = {}

    screenshot = get_map_screenshot(order.map)

    placeholders['_обзорная_схема'] = BytesIO(screenshot)

    return download_docx(request, document_name, document_path, document_cipher, placeholders)


# Получение скриншота карты
def get_map_screenshot(map_html):
    data_url = 'data:text/html;charset=utf-8,{}'.format(urlquote(map_html))

    driver = webdriver.Chrome()
    driver.set_window_size(1024, 748)
    driver.get(data_url)

    time.sleep(1)
    screenshot = driver.get_screenshot_as_png()
    driver.quit()

    return screenshot


# Скачивание карты
def download_map(request, pk):
    order = get_object_or_404(Order, pk=pk)

    screenshot_name = f"{datetime.datetime.now().strftime('%Y%m%d')}-{order.pk:03d}"
    screenshot = get_map_screenshot(order.map)

    response = HttpResponse(content_type='image/png')
    response['Content-Disposition'] = f'attachment; filename="{screenshot_name}.png"'
    response.write(screenshot)

    return response


# Скачивание координат
def download_xlsx(request, pk):
    order = get_object_or_404(Order, pk=pk)
    cadastral_numbers = order.cadastral_numbers

    coordinates_list = json.loads(order.coordinates)
    coordinates_dict = {}

    for i, coords in enumerate(coordinates_list):
        cadastral_num = cadastral_numbers[i]
        coordinates_dict[cadastral_num] = coords[0]

    # Создаем новый файл Excel
    workbook = openpyxl.Workbook()

    # Получаем лист по умолчанию
    sheet = workbook.active

    # Записываем заголовки строк
    current_row = 1

    # Проходим по каждому ключу словаря coordinates_dict
    for key, coords in coordinates_dict.items():
        # Записываем заголовок строки с координатами углов участка
        sheet.merge_cells(start_row=current_row, start_column=1, end_row=current_row, end_column=3)
        sheet.cell(row=current_row, column=1, value=f'Координаты углов участка {key}')
        current_row += 1

        # Записываем заголовки столбцов таблицы
        sheet.cell(row=current_row, column=1, value='Номер точки')
        sheet.cell(row=current_row, column=2, value='Координата Х')
        sheet.cell(row=current_row, column=3, value='Координата У')
        current_row += 1

        # Проходим по каждой координате в списке для данного ключа
        for i, coord in enumerate(coords):
            # Записываем номер точки, координату Х и координату У
            sheet.cell(row=current_row, column=1, value=str(i + 1))
            sheet.cell(row=current_row, column=2, value=str(coord[0]))
            sheet.cell(row=current_row, column=3, value=str(coord[1]))
            current_row += 1

        # Добавляем пустую строку между таблицами
        current_row += 1

    document_cipher = f"{datetime.datetime.now().strftime('%Y%m%d')}-{order.pk:03d}"

    # Сохраняем файл и отправляем его пользователю
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=coord.xlsx'
    response['Content-Disposition'] = f'attachment; filename="{document_cipher}-coord.xlsx"'
    workbook.save(response)

    return response