import datetime

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse

from .forms import OrderForm, OrderFileForm, OrderChangeStatusForm, CadastralNumberForm
from .models import OrderFile, TypeWork, Order
from django.contrib import messages
from django.utils.crypto import get_random_string

import io
import os
from docx import Document
from django.http import HttpResponse
from django.conf import settings

User = get_user_model()


def view_order_cadastral(request, company_slug, company_number_slug):
    context = {}
    if request.method == 'POST':
        form = CadastralNumberForm(request.POST)
        if form.is_valid():
            cadastral_number = request.POST.get('cadastral_number')
            response = HttpResponseRedirect(reverse('zakaz:order', args=[company_slug, company_number_slug]))
            response.set_cookie('cadastral_number', cadastral_number)
            return response
    else:
        form = CadastralNumberForm

    context['form'] = form

    return render(request, 'customer_home.html', context=context)


@login_required(login_url='users:user_login')
def view_order(request, company_slug, company_number_slug):
    user_company = get_object_or_404(User, company_number_slug=company_number_slug)
    context = {
        'cadastral_number': request.COOKIES.get('cadastral_number')
    }
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        order_files_form = OrderFileForm(request.POST, request.FILES)
        if order_form.is_valid() and order_files_form.is_valid():
            order = order_form.save()
            order.user = user_company
            order.save()
            for file in request.FILES.getlist('file'):
                OrderFile.objects.create(order=order, file=file)
            messages.success(request, 'Ваша заявка отправлена')

            # return HttpResponseRedirect(reverse('zakaz:order', args=[company_id]))
            
    else:
        order_form = OrderForm()
        order_form.fields['cadastral_number'].initial = request.COOKIES.get('cadastral_number')
        order_files_form = OrderFileForm()

    context['user_company'] = user_company
    context['order_form'] = order_form
    context['order_files_form'] = order_files_form

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


def view_download(request):
    return render(request, 'download.html')


# Выгрузка DOCX
def replace_placeholders(paragraph, placeholders):
    for placeholder, value in placeholders.items():
        if placeholder in paragraph.text:
            for run in paragraph.runs:
                if placeholder in run.text:
                    run.text = run.text.replace(placeholder, value)


# Замена слов по ключам в параграфах, заголовках и таблицах
def replace_placeholders_in_document(document, placeholders):
    for paragraph in document.paragraphs:
        replace_placeholders(paragraph, placeholders)

    for table in document.tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    replace_placeholders(paragraph, placeholders)

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


# Скачиваем ШИФР-ИГДИ
def download_igdi_docx(request):
    document_name = 'igdi'
    document_path = os.path.join(settings.MEDIA_ROOT, f'{document_name}.docx')
    placeholders = {
        '_шифр-игди': 'Какой-то шифр ИГДИ',
        '_должность_руководителя_ведомства': 'Директор',
        '_название_ведомства': 'Ведомство всех ведомств',
        '_фио_руководителя_ведомства': 'Иванов Иван Иванович',
        '_тел_ведомства': '8 900 000 00 00',
        '_почта_ведомства': 'vedomstvo@example.com',
        '_дата_текущая': datetime.datetime.now().strftime("%Y-%m-%d"),
        '_имя_руководителя_ведомства': 'Иван',
        '_название_объекта_полное': 'Объект какой-то там',
        '_кадастровый_номер': '47:23:0604008:451',
        '_обзорная_схема': 'схема',
        '_таблица_координат': 'координаты'
    }
    return download_docx(request, document_name, document_path, placeholders)


# Скачиваем ШИФР-ИГИ
def download_igi_docx(request):
    document_name = 'igi'
    document_path = os.path.join(settings.MEDIA_ROOT, f'{document_name}.docx')
    placeholders = {
        '_шифр-иги': 'Какой-то шифр ИГИ',
        '_должность_руководителя_ведомства': 'Директор',
        '_название_ведомства': 'Ведомство всех ведомств',
        '_фио_руководителя_ведомства': 'Иванов Иван Иванович',
        '_тел_ведомства': '8 900 000 00 00',
        '_почта_ведомства': 'vedomstvo@example.com',
        '_дата_текущая': datetime.datetime.now().strftime("%Y-%m-%d"),
        '_имя_руководителя_ведомства': 'Иван',
        '_название_объекта_полное': 'Объект какой-то там',
        '_кадастровый_номер': '47:23:0604008:451',
        '_обзорная_схема': 'схема',
        '_таблица_координат': 'координаты'
    }
    return download_docx(request, document_name, document_path, placeholders)
