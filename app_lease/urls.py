from django.contrib import admin
from django.urls import path, include
from app_lease import views


urlpatterns = [
    path('services/', views.service_list),
]
