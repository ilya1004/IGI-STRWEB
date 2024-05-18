from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.urls import reverse
from django.utils import timezone, dateformat
from car_rental_service_app.models import *
from car_rental_service_app.forms import *
import random
import calendar
from datetime import datetime, timedelta
import logging

logger = logging.getLogger('db_logger')

def index(request: HttpRequest):
    time = timezone.datetime.now()
    user_timezone = request.session.get("django_timezone") 
    date = dateformat.format(time, "d/m/Y")
    cal = calendar.month(time.year, time.month)
    logger.info("Index page showed")
    new = News.objects.last()
    return render(request, "index.html", context={"date": date, "user_timezone": user_timezone, "new": new, "calendar": cal})


def about(request):
    about = AboutCompany.objects.first()
    logger.info("About page showed")
    return render(request, "company/about.html", context={"about": about})


def contacts(request):
    if request.method == "POST":
        if "edit_worker" in request.POST:
            worker_id = request.POST.get("edit_worker")
            return HttpResponseRedirect(f"/edit_worker/{worker_id}")
        elif "delete_worker" in request.POST:
            worker_id = request.POST.get("delete_worker")
            return HttpResponseRedirect(f"/delete_worker/{worker_id}")
        elif "add_worker" in request.POST:
            worker_id = request.POST.get("add_worker")
            return HttpResponseRedirect(f"/add_worker")
    else:
        workers = Worker.objects.all()
        logger.info("Contacts page showed")
        return render(request, "company/contacts.html", context={"workers": workers})


def discounts(request):
    if "edit_discount" in request.POST:
            discount_id = request.POST.get("edit_discount")
            return HttpResponseRedirect(f"/edit_discount/{discount_id}")
    elif "delete_discount" in request.POST:
            discount_id = request.POST.get("delete_discount")
            return HttpResponseRedirect(f"/delete_discount/{discount_id}")
    elif "add_discount" in request.POST:
            discount_id = request.POST.get("add_discount")
            return HttpResponseRedirect(f"/add_discount")
    else:
        discounts = Discount.objects.all()
        logger.info("Discounts page showed")
        return render(request, "discounts.html", {"discounts": discounts})


def glossary(request):
    terms = GlossaryQuestion.objects.all()
    logger.info("Glossary page showed")
    return render(request, "glossary.html", context={"terms": terms})


def privacy_policy(request):
    logger.info("Privacy policy page showed")
    return render(request, "company/privacy_policy.html")


def reviews(request):
    reviews = Review.objects.all()
    logger.info("Reviews page showed")
    return render(request, "reviews.html", {"reviews": reviews})


def add_review(request):
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            item = form.save()
            item.sender = request.user.client
            item.date = timezone.now()  
            item.save()
            logger.info("Review page showed")
            return redirect("reviews")
        else:
            logger.warning(f"Form is invalid")
            return render(request, "add_review.html", {"form": form}) 
    else:
        form = ReviewForm()
        return render(request, "add_review.html", {"form": form}) 


def vacancies(request):
    vacancies = Vacancy.objects.all()
    logger.info("Vacancies page showed")
    return render(request, "company/vacancies.html", context={"vacancies": vacancies})


def car_park(request: HttpRequest):
    logger.info("Car park page showed")
    if request.method == "POST":
        if "make_order" in request.POST:
            car_id = request.POST.get("make_order")
            return redirect(f"/make_order/{car_id}")
        elif "edit_car" in request.POST:
            car_id = request.POST.get("edit_car")
            return HttpResponseRedirect(f"/edit_car/{car_id}")
        elif "delete_car" in request.POST:
            car_id = request.POST.get("delete_car")
            return HttpResponseRedirect(f"/delete_car/{car_id}")
        elif "add_car" in request.POST:
            car_id = request.POST.get("add_car")
            return HttpResponseRedirect(f"/add_car")
        else:
            cars = Car.objects.all()
            form = FilterBodyTypeForm()
            return render(request, "car_park.html", context={"cars": cars, "form": form})

    elif request.method == "GET":
        cars = Car.objects.all()
        form = FilterBodyTypeForm(request.GET)
        if "body_type" in request.GET:
            if form.is_valid():
                if form.cleaned_data["body_type"] != None:
                    cars = cars.filter(body_type=form.cleaned_data["body_type"])
            else:
                logger.warning(f"Form is invalid")
        elif "sorting" in request.GET:
            print("qwe")
            sort_param = request.GET.get("sorting")
            if sort_param == "model":
                cars = list(cars.order_by("model"))
            elif sort_param == "price":
                cars = list(cars.order_by("price"))
            elif sort_param == "brand":
                cars = list(cars.order_by("brand"))
        
        return render(request, "car_park.html", context={"cars": cars, "form": form})        
    
    else:
        cars = Car.objects.all()
        form = FilterBodyTypeForm()
        return render(request, "car_park.html", context={"cars": cars, "form": form})
    


def make_order(request, car_id):
    logger.info("Making order page showed")
    if request.method == "POST":
        form = CarExtraditionForm(request.POST)
        if form.is_valid():
            item: CarExtradition = form.save()
            car = Car.objects.get(pk=int(car_id))
            car.is_ordered = True
            car.save()
            discount = None
            try:
                discount = Discount.objects.get(promocode=item.promocode)
            except Exception as e:
                discount = None
    
            item.discount = discount
            date_end = date(year=item.date_start.year, month=item.date_start.month, day=item.date_start.day) + timedelta(days=item.number_days)
            item.date_end = date_end
            item.car = car
            item.rental_amount = 0.0
            item.client = request.user.client
            
            item.worker = Worker.objects.get(pk=random.choice([2, 7]))
            item.set_rental_amount()
            item.save()
            return redirect(f"/success_order/{item.pk}")
        else:
            logger.warning(f"Form is invalid")
            return render(request, "user/make_order.html", {"form": form})
    
    else:
        form = CarExtraditionForm()
        return render(request, "user/make_order.html", {"form": form})
    

def success_order(request, order_id):
    logger.info("Order has been successfuly made")
    order = CarExtradition.objects.get(pk=order_id)
    return render(request, "user/success_order.html", {"order": order})


def fines(request: HttpRequest):
    if request.method == "POST":
        if "edit_fine" in request.POST:
            fine_id = request.POST.get("edit_fine")
            return HttpResponseRedirect(f"/edit_fine/{fine_id}")
        elif "delete_fine" in request.POST:
            fine_id = request.POST.get("delete_fine")
            return HttpResponseRedirect(f"/delete_fine/{fine_id}")
        elif "add_fine" in request.POST:
            fine_id = request.POST.get("add_fine")
            return HttpResponseRedirect(f"/add_fine")
    logger.info("Fines page showed")
    fines = Fine.objects.all()
    return render(request, "fines.html", {"fines": fines})