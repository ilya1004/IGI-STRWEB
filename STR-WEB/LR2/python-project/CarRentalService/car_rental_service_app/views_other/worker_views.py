from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from car_rental_service_app.forms import *
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.urls import reverse
from car_rental_service_app.models import *
import logging

logger = logging.getLogger('db_logger')

@login_required
def list_orders(request: HttpRequest):
    if request.method == "POST":
        order_id = request.POST.get("give_fine")
        return HttpResponseRedirect(f"/give_fine/{order_id}")
        
        
    lst = CarExtradition.objects.filter(worker=request.user.worker, is_active=True)
    fines = []
    for i in lst:
        fines.append(i.fines.all())
    
    logger.info("List orders showed for worker")
    data = [[lst[i], fines[i]] for i in range(len(lst))]
    return render(request, 'list_worker_orders.html', {'orders': data})


def give_fine(request: HttpRequest, order_id):
    order = CarExtradition.objects.get(pk=order_id)
    if request.method == "POST":
        form = GiveFineForm(request.POST)
        if form.is_valid():
            if form.cleaned_data["fine"] != None:
                fine = Fine.objects.get(name=form.cleaned_data["fine"])
                order.fines.add(fine)
                order.add_fine(fine)
                order.save()
                logger.info("Worker give fine to order")
            return HttpResponseRedirect(reverse("list_worker_orders"))
    else:
        form = GiveFineForm(request.POST)
        return render(request, "give_fine.html", context={"form": form})