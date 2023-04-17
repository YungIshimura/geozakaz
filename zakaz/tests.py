from django.test import TestCase, RequestFactory
from users.models import User
from django.template.defaultfilters import slugify
from django.contrib.auth import get_user_model, authenticate
from .models import *
from datetime import datetime
from selenium import webdriver
import time


class UserTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            password='12test12', email='test@example.com', phone_number='+79186782222')
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_correct(self):
        user = authenticate(email='test@example.com', password='12test12')
        self.assertTrue((user is not None) and user.is_authenticated)

    def test_wrong_username(self):
        user = authenticate(email='wrong@example.com', password='12test12')
        self.assertFalse(user is not None and user.is_authenticated)

    def test_wrong_pssword(self):
        user = authenticate(email='test@example.com', password='wrong')
        self.assertFalse(user is not None and user.is_authenticated)

    def test_user_has_slug(self):
        self.user.company_name = 'gfs'
        self.user.save()
        self.assertEqual(self.user.company_slug,
                         slugify(self.user.company_name))


class ModelTestCase(TestCase):
    def setUp(self):
        region = Region.objects.create(
            name='Красноярский край',
            cadastral_region_number = '24'
        )
        area = Area.objects.create(
            name='Ужурский район',
            cadastral_area_number='39',
            region=region
        )
        city = City.objects.create(
            name='Ужур',
            area=area
        )
        type_work = TypeWork.objects.create(
            type='Геодезия'
        )
        work_objective = WorkObjective.objects.create(
            objective='Тесты'
        )
        self.order = Order.objects.create(
            name='Алекс',
            surname='Алексов',
            father_name='Алексович',
            phone_number='+79182331111',
            email='mark@mark.com',
            cadastral_numbers=['24:39:0101001:369'],
            region=Region.objects.all().first(),
            area=Area.objects.all().first(),
            city=City.objects.all().first(),
            street='Гоголя',
            house_number=12,
            building=3,
            square=4.77,
            square_unit='hectometer',
            length=12,
            length_unit='m',
            width=12,
            width_unit='m',
            height=12,
            height_unit='m',
            comment='123',
            date=datetime.now(),
            purpose_building=PurposeBuilding.objects.all().first(),
            work_objective=WorkObjective.objects.all().first(),
            object_name='Банан'
        )
        self.order.type_work.set(str(TypeWork.objects.first().id))
        self.order.save()

    def test_incorrect_phone(self):
        phone_number = self.order.phone_number
        self.order.phone_number='askdgadasdg' 
        self.assertNotEqual(phone_number, self.order.phone_number)


    def test_incorrect_email(self):
        email = self.order.email
        self.order.email = 'akdgma'
        self.assertNotEqual(email, self.order.email)

    
class ZakazTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            password='12test12', email='test@example.com', phone_number='+79181673151', company_name='ммм', company_number_slug='123123')

        self.user.is_active=True
        self.user.is_staff=True
        self.user.save()

        region = Region.objects.create(
            name='Красноярский край',
            cadastral_region_number = '24'
        )
        area = Area.objects.create(
            name='Ужурский район',
            cadastral_area_number='39',
            region=region
        )
        city = City.objects.create(
            name='Ужур',
            area=area
        )
        region.save()
        area.save()
        city.save()

    def test_order_page(self):
        response = self.client.get('http://127.0.0.1:8000/order/mmm/123123/')
        self.assertEqual(response.status_code, 200)

    def test_order_page_form_with_cadastral_numbers(self):
        session = self.client.session
        session['cadastral_numbers'] = ['24:39:0101001:369']
        session.save()
        response = self.client.get('http://127.0.0.1:8000/order/mmm/123123/form/')
        self.assertEqual(response.status_code, 200)

    def test_order_page_form_with_address(self):
        session = self.client.session
        session['address'] = ['Красноярский край, Ужурский район, Ужур']
        session.save()
        response = self.client.get('http://127.0.0.1:8000/order/mmm/123123/form/')
        self.assertEqual(response.status_code, 200)

    def test_order_pages(self):
        self.client.login(email='test@example.com', password='12test12')
        response = self.client.get('http://127.0.0.1:8000/order_pages/123123/')
        self.assertEqual(response.status_code, 200)