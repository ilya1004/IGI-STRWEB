from django.db import models
from django.contrib.auth.models import User
from datetime import date, datetime, timedelta
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    email = models.EmailField(max_length=40, default="user@email.by")
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    patronymic = models.CharField(max_length=30)    
    address = models.CharField(max_length=70)
    phone_number = models.CharField(max_length=20, validators=[RegexValidator(regex=r'^\+\d{9,14}$',message="Вы ввели некорректный номер телефона")])
    birthday_date = models.DateField(default="2000-01-01", validators=[MaxValueValidator(date.today() - timedelta(days=18 * 365), 
                                                                                         message="Для регистрации необходимо достичь 18 лет")])
    image = models.ImageField(upload_to="clients", default="clients/default_avatar.jpg")
    age = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(150)], default=0)


class CarBrand(models.Model):
    name = models.CharField(max_length=30)
    
    def __str__(self):
        return self.name


class CarBodyType(models.Model):
    name = models.CharField(max_length=30)
    
    def __str__(self):
        return self.name


class Car(models.Model):
    number = models.CharField(max_length=20)
    brand = models.ForeignKey(CarBrand, on_delete=models.CASCADE)
    body_type = models.ForeignKey(CarBodyType, on_delete=models.CASCADE)
    model = models.CharField(max_length=30)
    year = models.IntegerField(validators=[MinValueValidator(1900), MaxValueValidator(2024)])
    price = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0)])
    daily_price = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0)])
    is_ordered = models.BooleanField(default=False)


class Discount(models.Model):
    name = models.CharField(max_length=30)
    percent = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(100)])
    promocode = models.CharField(max_length=30)
    
    
class Fine(models.Model): # штраф
    name = models.CharField(max_length=30)
    amount = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(1000)])
    
    def __str__(self):
        return self.name


class Worker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    email = models.EmailField(max_length=40, default="worker@email.by")
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    position = models.CharField(max_length=50) # должность
    work_description = models.CharField(max_length=500, default="")
    phone_number = models.CharField(max_length=20, validators=[RegexValidator(regex=r'^\+\d{9,14}$', message="Вы ввели некорректный номер телефона")])
    image = models.ImageField(upload_to="contacts", default="contacts/default_avatar.jpg")


class CarExtradition(models.Model):
    date_start = models.DateField(auto_now=False, auto_now_add=False, validators=[MaxValueValidator(datetime.now().date())])
    date_end = models.DateField(auto_now=False, auto_now_add=False, null=True)
    number_days = models.IntegerField(validators=[MinValueValidator(0)])
    rental_amount = models.DecimalField(max_digits=8, decimal_places=2, null=True, default=0)
    promocode = models.CharField(max_length=30, null=True)
    discount_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    fine_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    final_sum = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, null=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="list_extraditions", null=True)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, null=True)
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE, null=True, blank=True)
    fines = models.ManyToManyField(Fine, blank=True)
    is_active = models.BooleanField(default=True)
    
    def set_rental_amount(self):
        self.rental_amount = self.number_days * self.car.daily_price
        if not self.discount is None:
            amount = self.rental_amount * (self.discount.percent / 100)
            self.discount_amount = amount
            self.final_sum = self.rental_amount - amount
        else:
            self.final_sum = self.rental_amount
    
    def add_fine(self, fine: Fine):
        self.fine_amount += fine.amount
        self.final_sum += fine.amount


class CompanyInfo(models.Model):
    name = models.CharField(max_length=100, default="")
    text = models.TextField()
    logo = models.ImageField(upload_to="images", default="news/no_image.jpg")
    video_src = models.CharField(max_length=200, default="")
    history = models.JSONField(default=dict)
    requisites = models.TextField(default="")
    certificate = models.TextField(default="")      
    

class News(models.Model):
    title = models.CharField(max_length=200, default="")
    short_description = models.CharField(max_length=500, default="")
    url = models.URLField(max_length=200, default="")
    text = models.TextField(default="")
    image = models.ImageField(upload_to="news", default="news/no_image.png")
    image_url = models.URLField(max_length=1000, null=True)
    

class GlossaryQuestion(models.Model):
    question = models.CharField(max_length=200)
    response = models.CharField(max_length=500)
    date = models.DateField(auto_now=False, auto_now_add=False, null=True)
    

class Vacancy(models.Model):
    position = models.CharField(max_length=50) # должность
    description = models.CharField(max_length=500)


class Review(models.Model):
    sender = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100)
    rate = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    text = models.CharField(max_length=500)
    date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True)


class PartnerCompany(models.Model):
    name = models.CharField(max_length=50)
    site_url = models.URLField(max_length=200)
    image = models.ImageField(upload_to="partners", default="news/no_image.png")