from django.contrib import admin
from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from car_rental_service_app import views
from car_rental_service_app.views_other import api_views, user_views, worker_views, admin_views

urlpatterns = [
    path("admin/", admin.site.urls, name="admin"),
    path("", views.index, name="home"),
    re_path(r"^about/$", views.about, name="about"),
    re_path(r"^contacts/$", views.contacts, name="contacts"),
    re_path(r"^discounts/$", views.discounts, name="discounts"),
    re_path(r"^glossary/$", views.glossary, name="glossary"),
    re_path(r"^news/$", api_views.news, name="news"),
    re_path(r"^privacy_policy/$", views.privacy_policy, name="privacy_policy"),
	re_path(r"^reviews/$", views.reviews, name="reviews"),
    re_path(r"^add_review/$", views.add_review, name="add_review"),
	re_path(r"^vacancies/$", views.vacancies, name="vacancies"),
    re_path(r"^cat_facts/$", api_views.cat_facts, name="cat_facts"),
    re_path(r"^fines/$", views.fines, name="fines"),
    re_path(r"^give_fine/(\d+)$", worker_views.give_fine, name="give_fine"),
    
    re_path(r"^accounts/register/$", user_views.register, name="register"),
    re_path(r"^accounts/profile/$", user_views.profile, name="profile"),
    re_path(r"^accounts/login/$", user_views.login, name="login"),
    re_path(r"^accounts/logout/$", user_views.logout, name="logout"),
    re_path(r"^accounts/change_pass/$", user_views.change_password, name="change_pass"),
    re_path(r"^accounts/edit_profile/$", user_views.edit_profile, name="edit_profile"),
    
    re_path(r"^car_park/$", views.car_park, name="car_park"),
    re_path(r"^make_order/(\d+)$", views.make_order, name="make_order"),
    re_path(r"^success_order/(\d+)$", views.success_order, name="success_order"),
    re_path(r"^list_orders/$", user_views.list_orders, name="list_orders"),
    re_path(r"^list_worker_orders/$", worker_views.list_orders, name="list_worker_orders"),
    
    re_path(r"^add_car/$", admin_views.add_car, name="add_car"),
    re_path(r"^edit_car/(\d+)$", admin_views.edit_car, name="edit_car"),
    re_path(r"^delete_car/(\d+)$", admin_views.delete_car, name="delete_car"),
    
    re_path(r"^add_worker/$", admin_views.add_worker, name="add_worker"),
    re_path(r"^edit_worker/(\d+)$", admin_views.edit_worker, name="edit_worker"),
    re_path(r"^delete_worker/(\d+)$", admin_views.delete_worker, name="delete_worker"),
    
    re_path(r"^add_discount/$", admin_views.add_discount, name="add_discount"),
    re_path(r"^edit_discount/(\d+)$", admin_views.edit_discount, name="edit_discount"),
    re_path(r"^delete_discount/(\d+)$", admin_views.delete_discount, name="delete_discount"),
    
    re_path(r"^list_users/$", admin_views.list_users, name="list_users"),
    re_path(r"^edit_user/(\d+)$", admin_views.edit_user, name="edit_user"),
    re_path(r"^delete_user/(\d+)$", admin_views.delete_user, name="delete_user"),
    
    re_path(r"^list_car_brands/$", admin_views.list_car_brands, name="list_car_brands"),
    re_path(r"^add_car_brand/$", admin_views.add_car_brand, name="add_car_brand"),
    re_path(r"^edit_car_brand/(\d+)$", admin_views.edit_car_brand, name="edit_car_brand"),
    re_path(r"^delete_car_brand/(\d+)$", admin_views.delete_car_brand, name="delete_car_brand"),
    
    re_path(r"^list_body_types/$", admin_views.list_body_types, name="list_body_types"),
    re_path(r"^add_body_type/$", admin_views.add_body_type, name="add_body_type"),
    re_path(r"^edit_body_type/(\d+)$", admin_views.edit_body_type, name="edit_body_type"),
    re_path(r"^delete_body_type/(\d+)$", admin_views.delete_body_type, name="delete_body_type"),
    
    re_path(r"^add_fine/$", admin_views.add_fine, name="add_fine"),
    re_path(r"^edit_fine/(\d+)$", admin_views.edit_fine, name="edit_fine"),
    re_path(r"^delete_fine/(\d+)$", admin_views.delete_fine, name="delete_fine"),
    
    re_path(r"^statistics/$", admin_views.statistics, name="statistics"),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
