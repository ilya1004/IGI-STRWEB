from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from car_rental_service_app.models import *

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "password1", "password2") 


class ClientRegistrationForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ("email", "name", "surname", "patronymic", "address", "phone_number", "birthday_date", "image")
        widgets = {"birthday_date": forms.DateInput(attrs={"class":"form-control", "type":"date"}),
                   "image": forms.FileInput(attrs={"class": "form-control", "required": False})}


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ("title", "rate", "text")


class CarExtraditionForm(forms.ModelForm):
    class Meta:
        model = CarExtradition
        fields = ("date_start", "number_days", "promocode")
        widgets = {"date_start": forms.DateInput(attrs={"class":"form-control", "type":"date"})}


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ("brand", "body_type", "model", "year", "price", "daily_price")


class WorkerForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = ("email", "name", "surname", "position", "work_description", "phone_number", "image")
        widgets = {"image": forms.FileInput(attrs={"class": "form-control", "required": False})}


class DiscountForm(forms.ModelForm):
    class Meta:
        model = Discount
        fields = ("name", "percent", "promocode")


class CarBrandForm(forms.ModelForm):
    class Meta:
        model = CarBrand
        fields = ("name",)


class CarBodyTypeForm(forms.ModelForm):
    class Meta:
        model = CarBodyType
        fields = ("name",)


class FilterBodyTypeForm(forms.Form):
    body_type = forms.ModelChoiceField(queryset=CarBodyType.objects.all(), required=False)
    

class FineForm(forms.ModelForm):
    class Meta:
        model = Fine
        fields = ("name", "amount")


class GiveFineForm(forms.Form):
    fine = forms.ModelChoiceField(queryset=Fine.objects.all(), required=False)