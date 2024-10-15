from django.shortcuts import render, redirect
from car_rental_service_app.forms import ClientRegistrationForm, RegistrationForm, LoginForm
from django.contrib.auth import login as django_login, logout as django_logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpRequest
from django.urls import reverse
from car_rental_service_app.models import *
import logging

logger = logging.getLogger('db_logger')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        profile_form = ClientRegistrationForm(request.POST, request.FILES)
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            client = profile_form.save()
            user.save()
            client.user = user
            client.save()
            logger.info("User registered")
            django_login(request, user)
            return HttpResponseRedirect(reverse('profile'))
        else:
            return render(request, 'user/register.html', {'form': form, "profile_form": profile_form})
    else:
        form = RegistrationForm()
        profile_form = ClientRegistrationForm(request.POST, request.FILES)
        return render(request, 'user/register.html', {'form': form, "profile_form": profile_form})


@login_required
def profile(request):
    user = request.user
    is_worker = False
    if request.user.is_superuser:
        is_worker = True
        return HttpResponseRedirect(reverse('home'))
    try:
        profile = user.client
        is_worker = False
    except:
        is_worker = True
        profile = None
    
    if profile is None:
        profile = user.worker
        is_worker = True
    
    if request.user.is_superuser:
        is_worker = True

    phone_number = ""
    if profile.phone_number.startswith("+375"):
        phone_number = f"+375 ({profile.phone_number[4:6]}) {profile.phone_number[6:9]}-{profile.phone_number[9:11]}-{profile.phone_number[11:13]}"

    logger.info("User profile showed")

    data = {'profile': profile, 'is_worker': is_worker, "phone_number": phone_number}
    return render(request, 'user/profile.html', data)


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.data
            user = authenticate(request, username=data["username"], password=data["password"])
            if user is not None:
                logger.info("User successfuly login")
                django_login(request, user)
                return HttpResponseRedirect(reverse('home'))
            else:
                messages.error(request, 'Неверное имя пользователя или пароль.')
                return render(request, 'user/login.html', {'form': form})
        else:
            return render(request, 'user/login.html', {'form': form})
    else:
        form = LoginForm()
        return render(request, 'user/login.html', {'form': form})
    
    
@login_required
def logout(request):
    django_logout(request)
    logger.info("User successfuly logout")
    return HttpResponseRedirect(reverse('login'))


@login_required
def list_orders(request: HttpRequest):
    if request.method == "POST":
        order_id = request.POST.get("return_car")
        order: CarExtradition = CarExtradition.objects.get(pk=order_id)
        order.is_active = False
        order.save()
        car = order.car
        car.is_ordered = False
        car.save()
        logger.info("List orders showed")
        lst = CarExtradition.objects.filter(client=request.user.client, is_active=True)
        return render(request, 'user/list_orders.html', {'orders': lst})
        
    lst = CarExtradition.objects.filter(client=request.user.client, is_active=True)
    return render(request, 'user/list_orders.html', {'orders': lst})


@login_required
def change_password(request: HttpRequest):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, data=request.POST)
        if form.is_valid():
            form.save()
            logger.info("Password has been successfuly changed")
            update_session_auth_hash(request, form.user)
            messages.success(request, "Пароль был успешно изменен")
            return redirect(profile)
    else:
        form = PasswordChangeForm(request.user)
        return render(request, "user/change_pass.html", {"form": form})
    

@login_required
def edit_profile(request: HttpRequest):
    if request.method == "POST":
        user_data = request.user.client
        form = ClientRegistrationForm(request.POST, request.FILES, instance=user_data)
        if form.is_valid():
            form.save()
            logger.info("User profile has been saved")
            messages.success(request, "Профиль был успешно изменен")
            return redirect(profile)
        else:
            return render(request, 'user/edit_profile.html', {'form': form})
            
    else:
        user_data = request.user.client
        form = ClientRegistrationForm(instance=user_data)
        return render(request, 'user/edit_profile.html', {'form': form})