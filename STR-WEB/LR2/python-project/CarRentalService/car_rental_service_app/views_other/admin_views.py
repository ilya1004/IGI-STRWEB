from django.shortcuts import render, redirect
from car_rental_service_app.forms import *
from django.contrib.auth import login as django_login, logout as django_logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.db.models import Sum, Avg, Count
from statistics import mode, median, mean
from django.urls import reverse
from car_rental_service_app.models import *
import plotly.graph_objs as draw
import datetime
import logging

logger = logging.getLogger('db_logger')

def statistics(request: HttpRequest):
    clients = Client.objects.all().order_by("surname")
    orders = CarExtradition.objects.all().order_by("car").order_by("car")
    
    total_sum = CarExtradition.objects.aggregate(total_sum=Sum('final_sum'))["total_sum"]
    
    sales = CarExtradition.objects.values_list("final_sum", flat=True)
    
    sales_average = mean(sales)
    sales_mode = mode(sales)
    sales_median = median(sales)
    
    ages = [((date.today() - client.birthday_date).days // 365) for client in clients]
    age_average = mean(ages)
    age_median = median(ages)
    
    popular_brand = CarBrand.objects.annotate(num_orders=Count('car')).order_by('num_orders').first()
    profitable_brand = CarBrand.objects.annotate(total_sales=Sum('car__carextradition__final_sum')).order_by('-total_sales').first()
    
    ages = [(18, 25), (26, 60), (61, 100)]
    for client in clients:
        if client.age == 0:
            client.age = int((datetime.date.today() - client.birthday_date).days // 365)
            client.save()

    clients_groups = [Client.objects.filter(age__range=(start, end)).count() for start, end in ages]
    labels = ["Подростки (18 - 25)", "Взрослые (26 - 60)", "Пожилые (61 - 100)"]
    
    figure = draw.Figure(data=[draw.Pie(labels=labels, values=clients_groups)]).to_html(full_html=False)
    
    logger.info("Showing statistics")
    
    data = {"clients": clients, "orders": orders, "total_sum": total_sum, 
            "sales_average": sales_average, "sales_mode": sales_mode, "sales_median": sales_median,
            "age_average": age_average, "age_median": age_median, "popular_brand": popular_brand,
            "profitable_brand": profitable_brand, "figure": figure}

    return render(request, 'admin/statistics.html', context=data)




# car

def add_car(request: HttpRequest):
    if request.method == "POST":
        form = CarForm(request.POST)
        if form.is_valid():
            new_car = form.save()
            new_car.save()
            logger.info("Added car")
            return HttpResponseRedirect(reverse("car_park"))
        else:
            logger.warning(f"Form is invalid")
            return render(request, 'admin/add_car.html', {"form": form})
    else:
        form = CarForm()
        brands = CarBrand.objects.all()
        body_types = CarBodyType.objects.all()
        return render(request, 'admin/add_car.html', {"form": form, "brands": brands, "body_types": body_types})


def edit_car(request: HttpRequest, car_id):
    if request.method == "POST":
        car = Car.objects.get(pk=car_id)
        form = CarForm(request.POST, instance=car)
        if form.is_valid():
            edited_car = form.save()
            edited_car.save()
            logger.info("Edited car")
            return HttpResponseRedirect(reverse("car_park"))
        else:
            logger.warning(f"Form is invalid")
            car = Car.objects.get(pk=car_id)
            form = CarForm(instance=car)
            return render(request, 'admin/edit_car.html', {"form": form})
    else:
        car = Car.objects.get(pk=car_id)
        form = CarForm(instance=car)
        return render(request, 'admin/edit_car.html', {"form": form})


def delete_car(request: HttpRequest, car_id):
    car = Car.objects.get(pk=car_id)
    car.delete()
    logger.info("Car deleted")
    return HttpResponseRedirect(reverse("car_park"))


# worker

def add_worker(request: HttpRequest):
    if request.method == "POST":
        form = WorkerForm(request.POST, files=request.FILES)
        user_form = RegistrationForm(request.POST)
        if form.is_valid() and user_form.is_valid():
            new_user = user_form.save()
            new_user.save()
            new_worker = form.save()
            new_worker.user = new_user
            new_worker.save()
            logger.info("Worker added")
            return HttpResponseRedirect(reverse("contacts"))
        else:
            logger.warning(f"Form is invalid")
            return render(request, 'admin/add_worker.html', {"form": form, "user_form": user_form})
    else:
        form = WorkerForm()
        user_form = RegistrationForm()
        return render(request, 'admin/add_worker.html', {"form": form, "user_form": user_form})
    
    
def edit_worker(request: HttpRequest, worker_id):
    if request.method == "POST":
        worker = Worker.objects.get(pk=worker_id)
        form = WorkerForm(request.POST, instance=worker, files=request.FILES)
        if form.is_valid():
            edited_worker = form.save()
            edited_worker.save()
            logger.info("Worker edited")
            return HttpResponseRedirect(reverse("contacts"))
        else:
            logger.warning(f"Form is invalid")
            worker = Worker.objects.get(pk=worker_id)
            form = WorkerForm(instance=worker)
            return render(request, 'admin/edit_worker.html', {"form": form})
    else:
        worker = Worker.objects.get(pk=worker_id)
        form = WorkerForm(instance=worker)
        return render(request, 'admin/edit_worker.html', {"form": form})


def delete_worker(request: HttpRequest, worker_id):
    worker = Worker.objects.get(pk=worker_id)
    user_id = worker.user.pk
    user = User.objects.get(pk=user_id)
    user.delete()
    worker.delete()
    logger.info("Worker deleted")
    return HttpResponseRedirect(reverse("contacts"))


# discount

def add_discount(request: HttpRequest):
    if request.method == "POST":
        form = DiscountForm(request.POST)
        if form.is_valid():
            new_discount = form.save()
            new_discount.save()
            logger.info("Discount added")
            return HttpResponseRedirect(reverse("discounts"))
        else:
            logger.warning(f"Form is invalid")
            return render(request, 'admin/add_discount.html', {"form": form})
    else:
        form = DiscountForm()
        return render(request, 'admin/add_discount.html', {"form": form})
    
    
def edit_discount(request: HttpRequest, discount_id):
    if request.method == "POST":
        discount = Discount.objects.get(pk=discount_id)
        form = DiscountForm(request.POST, instance=discount)
        if form.is_valid():
            edited_discount = form.save()
            edited_discount.save()
            logger.info("Discount edited")
            return HttpResponseRedirect(reverse("discounts"))
        else:
            logger.warning(f"Form is invalid")
            discount = Discount.objects.get(pk=discount_id)
            form = DiscountForm(instance=discount)
            return render(request, 'admin/edit_discount.html', {"form": form})
    else:
        discount = Discount.objects.get(pk=discount_id)
        form = DiscountForm(instance=discount)
        return render(request, 'admin/edit_discount.html', {"form": form})


def delete_discount(request: HttpRequest, discount_id):
    worker = Discount.objects.get(pk=discount_id)
    worker.delete()
    logger.info("Discount deleted")
    return HttpResponseRedirect(reverse("discounts"))


# user

def list_users(request: HttpRequest):
    if "edit_user" in request.POST:
            user_id = request.POST.get("edit_user")
            return HttpResponseRedirect(f"/edit_user/{user_id}")
    elif "delete_user" in request.POST:
            user_id = request.POST.get("delete_user")
            return HttpResponseRedirect(f"/delete_user/{user_id}")

    clients = Client.objects.all()
    lst = []
    for client in clients:
        orders = CarExtradition.objects.filter(client=client, is_active=True)
        sum = 0
        for order in orders:
            sum += order.final_sum
        lst.append(sum)

    data = [[clients[i], lst[i]] for i in range(len(clients))]
    logger.info("Showing users list")
    return render(request, 'admin/list_users.html', {"data": data})


def edit_user(request: HttpRequest, user_id):
    if request.method == "POST":
        client = Client.objects.get(pk=user_id)
        form = ClientRegistrationForm(request.POST, instance=client)
        if form.is_valid():
            edited_client = form.save()
            edited_client.save()
            logger.info("User edited")
            return HttpResponseRedirect(reverse("list_users"))
        else:
            logger.warning(f"Form is invalid")
            client = Client.objects.get(pk=user_id)
            form = ClientRegistrationForm(instance=client)
            return render(request, 'admin/edit_user.html', {"form": form})
    else:
        client = Client.objects.get(pk=user_id)
        form = ClientRegistrationForm(instance=client)
        return render(request, 'admin/edit_user.html', {"form": form})


def delete_user(request: HttpRequest, user_id):
    client = Client.objects.get(pk=user_id)
    orders: list[CarExtradition] = CarExtradition.objects.filter(client=client)
    for order in orders:
        car = order.car 
        car.is_ordered = False
        car.save()
        order.is_active = False
        order.save()
    
    logger.info("User deleted")
    client.delete()
    return HttpResponseRedirect(reverse("list_users"))


# car brands

def list_car_brands(request: HttpRequest):
    if "edit_car_brand" in request.POST:
            car_brand_id = request.POST.get("edit_car_brand")
            return HttpResponseRedirect(f"/edit_car_brand/{car_brand_id}")
    elif "delete_car_brand" in request.POST:
            car_brand_id = request.POST.get("delete_car_brand")
            return HttpResponseRedirect(f"/delete_car_brand/{car_brand_id}")
    elif "add_car_brand" in request.POST:
            car_brand_id = request.POST.get("add_car_brand")
            return HttpResponseRedirect(f"/add_car_brand")
        
    logger.info("Car brand deleted")
    car_brands = CarBrand.objects.all()
    return render(request, 'admin/list_car_brands.html', {"items": car_brands})


def add_car_brand(request: HttpRequest):
    if request.method == "POST":
        form = CarBrandForm(request.POST)
        if form.is_valid():
            new_car_brand = form.save()
            new_car_brand.save()
            logger.info("Car brand added")
            return HttpResponseRedirect(reverse("list_car_brands"))
        else:
            logger.warning(f"Form is invalid")
            return render(request, 'admin/add_car_brand.html', {"form": form})
    else:
        form = CarBrandForm()
        return render(request, 'admin/add_car_brand.html', {"form": form})
    
    
def edit_car_brand(request: HttpRequest, car_brand_id):
    if request.method == "POST":
        car_brand = CarBrand.objects.get(pk=car_brand_id)
        form = CarBrandForm(request.POST, instance=car_brand)
        if form.is_valid():
            edited_car_brand = form.save()
            edited_car_brand.save()
            logger.info("Car brand edited")
            return HttpResponseRedirect(reverse("list_car_brands"))
        else:
            logger.warning(f"Form is invalid")
            car_brand = CarBrand.objects.get(pk=car_brand_id)
            form = CarBrandForm(instance=car_brand)
            return render(request, 'admin/edit_car_brand.html', {"form": form})
    else:
        car_brand = CarBrand.objects.get(pk=car_brand_id)
        form = CarBrandForm(instance=car_brand)
        return render(request, 'admin/edit_car_brand.html', {"form": form})


def delete_car_brand(request: HttpRequest, car_brand_id):
    car_brand = CarBrand.objects.get(pk=car_brand_id)
    car_brand.delete()
    logger.info("Car brand deleted")
    return HttpResponseRedirect(reverse("list_car_brands"))



# body types


def list_body_types(request: HttpRequest):
    if "edit_body_type" in request.POST:
        body_type_id = request.POST.get("edit_body_type")
        return HttpResponseRedirect(f"/edit_body_type/{body_type_id}")
    elif "delete_body_type" in request.POST:
        body_type_id = request.POST.get("delete_body_type")
        return HttpResponseRedirect(f"/delete_body_type/{body_type_id}")
    elif "add_body_type" in request.POST:
        body_type_id = request.POST.get("add_body_type")
        return HttpResponseRedirect(f"/add_body_type")
    body_types = CarBodyType.objects.all()
    logger.info("Car body types list showed")
    return render(request, 'admin/list_body_types.html', {"items": body_types})


def add_body_type(request: HttpRequest):
    if request.method == "POST":
        form = CarBodyTypeForm(request.POST)
        if form.is_valid():
            new_body_type = form.save()
            new_body_type.save()
            logger.info("Car body types added")
            return HttpResponseRedirect(reverse("list_body_types"))
        else:
            logger.warning(f"Form is invalid")
            return render(request, 'admin/add_car_body_type.html', {"form": form})
    else:
        form = CarBodyTypeForm()
        return render(request, 'admin/add_car_body_type.html', {"form": form})
    
    
def edit_body_type(request: HttpRequest, body_type_id):
    if request.method == "POST":
        body_type = CarBodyType.objects.get(pk=body_type_id)
        form = CarBodyTypeForm(request.POST, instance=body_type)
        if form.is_valid():
            edited_body_type = form.save()
            edited_body_type.save()
            logger.info("Car body types edited")
            return HttpResponseRedirect(reverse("list_body_types"))
        else:
            logger.warning(f"Form is invalid")
            body_type = CarBodyType.objects.get(pk=body_type_id)
            form = CarBodyTypeForm(instance=body_type)
            return render(request, 'admin/edit_car_body_type.html', {"form": form})
    else:
        body_type = CarBodyType.objects.get(pk=body_type_id)
        form = CarBodyTypeForm(instance=body_type)
        return render(request, 'admin/edit_car_body_type.html', {"form": form})


def delete_body_type(request: HttpRequest, body_type_id):
    body_type = CarBodyType.objects.get(pk=body_type_id)
    body_type.delete()
    logger.info("Car body types deleted")
    return HttpResponseRedirect(reverse("list_body_types"))


# fines

def add_fine(request: HttpRequest):
    if request.method == "POST":
        form = FineForm(request.POST)
        if form.is_valid():
            new_fine = form.save()
            new_fine.save()
            logger.info("Fine added")
            return HttpResponseRedirect(reverse("fines"))
        else:
            logger.warning(f"Form is invalid")
            return render(request, 'admin/add_fine.html', {"form": form})
    else:
        form = FineForm()
        return render(request, 'admin/add_fine.html', {"form": form})
    
    
def edit_fine(request: HttpRequest, fine_id):
    if request.method == "POST":
        fine = Fine.objects.get(pk=fine_id)
        form = FineForm(request.POST, instance=fine)
        if form.is_valid():
            edited_fine = form.save()
            edited_fine.save()
            logger.info("Fine edited")
            return HttpResponseRedirect(reverse("fines"))
        else:
            logger.warning(f"Form is invalid")
            fine = Fine.objects.get(pk=fine_id)
            form = FineForm(instance=fine)
            return render(request, 'admin/edit_fine.html', {"form": form})
    else:
        fine = Fine.objects.get(pk=fine_id)
        form = FineForm(instance=fine)
        return render(request, 'admin/edit_fine.html', {"form": form})


def delete_fine(request: HttpRequest, fine_id):
    fine = Fine.objects.get(pk=fine_id)
    fine.delete()
    logger.info("Fine deleted")
    return HttpResponseRedirect(reverse("fines"))

