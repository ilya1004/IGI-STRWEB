from django.test import TestCase
from django.contrib.auth import get_user_model
from django.test import Client as TestClient
from car_rental_service_app.models import *
import datetime
from datetime import date, timedelta
from car_rental_service_app.forms import *
from car_rental_service_app.views import *
from django.urls import reverse


class TestViews(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.user_model = get_user_model()
        cls.user_admin = cls.user_model.objects.create_superuser(username='admin')
        cls.admin = TestClient()
        cls.admin.force_login(cls.user_admin)

        cls.user_1 = cls.user_model.objects.create(username='user1', 
                                                   password='pass1')
        
        cls.client_1 = Client.objects.create(name='name1', 
                                             surname='surname1', 
                                             patronymic="patronymic1",
                                             email='qwe1@qwe.ru',
                                             address="address1",
                                             birthday_date=date.today() - timedelta(days=20 * 365),
                                             phone_number='+375291234567')
        cls.client_1.user = cls.user_1
        cls.client_test_1 = TestClient()
        cls.client_test_1.force_login(cls.user_1)

        cls.user_2 = cls.user_model.objects.create(username='user2',
                                                   password="pass2")
        
        cls.client_2 = Client.objects.create(name='name2', 
                                             surname='surname2', 
                                             patronymic="patronymic2",
                                             email='qwe2@qwe.ru',
                                             address="address2",
                                             birthday_date=date.today() - timedelta(days=40 * 365),
                                             phone_number='+375291234567')
        cls.client_2.user = cls.user_2
        cls.client_test_2 = TestClient()
        cls.client_test_2.force_login(cls.user_2)

        cls.brand_1 = CarBrand.objects.create(name="brand_1")
        cls.brand_2 = CarBrand.objects.create(name="brand_2")
        
        cls.body_type_1 = CarBodyType.objects.create(name="body_type_1")
        cls.body_type_2 = CarBodyType.objects.create(name="body_type_1")
    
        cls.discount_1 = Discount.objects.create(name="discount_1", percent=10.0, promocode="qwe")    
        cls.fine_1 = Fine.objects.create(name="fine_1", amount=15.0)
        
        cls.car_1 = Car.objects.create(number="QWE123",
                                       brand=cls.brand_1,
                                       body_type=cls.body_type_1,
                                       model="model1",
                                       year=2021,
                                       price=30000.0,
                                       daily_price=11.0,
                                       is_ordered=False)
        
        cls.car_2 = Car.objects.create(number="ZXC123",
                                       brand=cls.brand_2,
                                       body_type=cls.body_type_2,
                                       model="model2",
                                       year=2022,
                                       price=34000.0,
                                       daily_price=14.0,
                                       is_ordered=False)
         
        cls.user_worker_1 = cls.user_model.objects.create(username='worker1', password="pass1")
        cls.worker_1 = Worker.objects.create(name='name4',
                                                      surname='surname4', 
                                                      email='qwe4@qwe.ru',
                                                      position="position1",
                                                      work_description="qwe1",
                                                      phone_number='+375291111111')

        cls.worker_1.user = cls.user_worker_1
        cls.worker_test_1 = TestClient()
        cls.worker_test_1.force_login(cls.user_worker_1)
        
        cls.order_1 = CarExtradition.objects.create(
                                    date_start=date.today(),
                                    date_end=date.today() + timedelta(days=12),
                                    number_days=12,
                                    rental_amount=123,
                                    promocode="",
                                    discount_amount=0,
                                    fine_amount=0,
                                    final_sum=123,
                                    car=cls.car_1,
                                    client=cls.client_1,
                                    worker=cls.worker_1,
                                    discount=None,
                                    # fines=fines.set(),
                                    is_active=True)
        
        cls.order_2 = CarExtradition.objects.create(
                                    date_start=date.today(),
                                    date_end=date.today() + timedelta(days=45),
                                    number_days=45,
                                    rental_amount=465,
                                    promocode="",
                                    discount_amount=65,
                                    fine_amount=20,
                                    final_sum=420,
                                    car=cls.car_2,
                                    client=cls.client_2,
                                    worker=cls.worker_1,
                                    discount=None,
                                    # fines=[],
                                    is_active=False)
        
    def test_name_label(self):
        client = Client.objects.get(pk=1)
        field_label = client._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')
    
    def test_surname_label(self):
        client = Client.objects.get(pk=1)
        field_label = client._meta.get_field('surname').verbose_name
        self.assertEqual(field_label, 'surname')
    
    def test_email_max_length(self):
        client = Client.objects.get(pk=1)
        max_length = client._meta.get_field('email').max_length
        self.assertEqual(max_length, 40)

    def test_name_employee_label(self):
        employee = Worker.objects.get(pk=1)
        field_label = employee._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')
    
    def test_surname_employee_label(self):
        employee = Worker.objects.get(pk=1)
        field_label = employee._meta.get_field('surname').verbose_name
        self.assertEqual(field_label, 'surname')

    def test_email_max_employee_length(self):
        employee = Worker.objects.get(pk=1)
        max_length = employee._meta.get_field('email').max_length
        self.assertEqual(max_length, 40)
    
    
    def test_username_field_too_long(self):
        username = '_' * 200
        form_data = {'username': username}
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    def test_register_client_1(self):
        name = '_' * 12
        surname = '_' * 12
        patronymic = '_' * 12
        email = "qwe@qe.we"
        address = "qweqwe"
        phone_number = "+375291234567"
        birthday_date = date(2000, 1, 1)
        form_data = {'name': name, 
                     "surname": surname, 
                     "patronymic": patronymic, 
                     "email": email, 
                     "address": address,
                     "phone_number": phone_number,
                     "birthday_date": birthday_date}
        form = ClientRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    
    def test_register_client_2(self):
        name = '_' * 12
        surname = '_' * 12
        patronymic = '_' * 100
        email = "qwe@qe.we"
        address = "qweqwe"
        phone_number = "+375291234567"
        birthday_date = date(2000, 1, 1)
        form_data = {'name': name, 
                     "surname": surname, 
                     "patronymic": patronymic, 
                     "email": email, 
                     "address": address,
                     "phone_number": phone_number,
                     "birthday_date": birthday_date}
        form = ClientRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    
    def test_car_park(self):
        response = self.client.get(reverse('car_park'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'car_park.html')
        
    def test_add_review(self):
        response = self.client.get(reverse('add_review'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_review.html')
        
    def test_cat_facts(self):
        response = self.client.get(reverse('cat_facts'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cat_facts.html')
        
    def test_discounts(self):
        response = self.client.get(reverse('discounts'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'discounts.html')
    
    def test_fines(self):
        response = self.client.get(reverse('fines'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'fines.html')
    
    def test_give_fine_1(self):
        response = self.client.get(reverse('give_fine', args=[self.order_1.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'give_fine.html')
    
    def test_give_fine_2(self):
        response = self.client.get(reverse('give_fine', args=[self.order_2.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'give_fine.html')
    
    def test_glossary(self):
        response = self.client.get(reverse('glossary'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'glossary.html')
    
    def test_news(self):
        response = self.client.get(reverse('news'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'news.html')
        
    def test_reviews(self):
        response = self.client.get(reverse('reviews'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reviews.html')



    def test_add_car(self):
        response = self.client.get(reverse('add_car'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/add_car.html')
    
    def test_edit_car(self):
        response = self.client.get(reverse('edit_car', args=[self.car_1.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/edit_car.html')
    
    def test_delete_car(self):
        response = self.client.get(reverse('delete_car', args=[self.car_1.pk]))
        self.assertEqual(response.status_code, 302)
    
    
    def test_add_car_brand(self):
        response = self.client.get(reverse('add_car_brand'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/add_car_brand.html')
    
    def test_edit_car_brand(self):
        response = self.client.get(reverse('edit_car_brand', args=[self.brand_1.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/edit_car_brand.html')
    
    def test_delete_car_brand(self):
        response = self.client.get(reverse('delete_car_brand', args=[self.brand_1.pk]))
        self.assertEqual(response.status_code, 302)
    
    
    def test_add_discount(self):
        response = self.client.get(reverse('add_discount'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/add_discount.html')
    
    def test_edit_discount(self):
        response = self.client.get(reverse('edit_discount', args=[self.discount_1.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/edit_discount.html')
    
    def test_delete_discount(self):
        response = self.client.get(reverse('delete_discount', args=[self.discount_1.pk]))
        self.assertEqual(response.status_code, 302)

    
    def test_add_fine(self):
        response = self.client.get(reverse('add_fine'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/add_fine.html')
    
    def test_edit_fine(self):
        response = self.client.get(reverse('edit_fine', args=[self.fine_1.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/edit_fine.html')
    
    def test_delete_fine(self):
        response = self.client.get(reverse('delete_fine', args=[self.fine_1.pk]))
        self.assertEqual(response.status_code, 302)
    
    
    def test_add_worker(self):
        response = self.client.get(reverse('add_worker'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/add_worker.html')
    
    def test_edit_worker(self):
        response = self.client.get(reverse('edit_worker', args=[self.worker_1.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/edit_worker.html')
    


    def test_profile(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)
    
    def test_login(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        
    
    def test_login_client_1(self):
        username = "qwe"
        password = "qwe"
        form_data = {'username': username, 
                     "password": password}
        form = LoginForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    
    def test_change_pass(self):
        response = self.client.get(reverse('change_pass'))
        self.assertEqual(response.status_code, 302)
    
    def test_edit_profile(self):
        response = self.client.get(reverse('edit_profile'))
        self.assertEqual(response.status_code, 302)
    
    def test_make_order(self):
        response = self.client.get(reverse('make_order', args=[self.car_1.pk]))
        self.assertEqual(response.status_code, 200)
    
    def test_register(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
    
    def test_success_order(self):
        response = self.client.get(reverse('success_order', args=[self.order_1.pk]))
        self.assertEqual(response.status_code, 200)
    
    
    def test_edit_index(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
    
    def test_edit_about(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'company/about.html')
    
    def test_edit_contacts(self):
        response = self.client.get(reverse('contacts'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'company/contacts.html')
    
    def test_edit_privacy_policy(self):
        response = self.client.get(reverse('privacy_policy'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'company/privacy_policy.html')
    
    def test_edit_vacancies(self):
        response = self.client.get(reverse('vacancies'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'company/vacancies.html')
    
    
    def test_logout(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
    
    def test_list_orders(self):
        response = self.client.get(reverse('list_orders'))
        self.assertEqual(response.status_code, 302)
        
    def test_car_brand_str(self):
        car_brand = str(self.brand_1)
        self.assertEqual(car_brand, self.brand_1.name)
    
    def test_car_bt_str(self):
        car_bt = str(self.body_type_1)
        self.assertEqual(car_bt, self.body_type_1.name)
    
    def test_fine_str(self):
        fine = str(self.fine_1)
        self.assertEqual(fine, self.fine_1.name)
    
    def test_qwe_1(self):
        n = str(self.order_1.set_rental_amount())
        self.assertEqual(n, "None")
    
    def test_qwe_2(self):
        n = str(self.order_1.add_fine(self.fine_1))
        self.assertEqual(n, "None")