from django.urls import path, include

import app_lease.api.user_api
from app_lease import api
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', api.UserViewSet)
router.register(r'groups', api.GroupViewSet)


urlpatterns = [



    # ----- API User
    path('register/', app_lease.api.user_register, name='api_register'),
    path('password_update/<int:pk>', app_lease.api.user_password_update,
         name='api_password_update'),
    path('login/', app_lease.api.user_login, name='api_login'),
    path('users/', app_lease.api.user_list, name='user_list'),
    path('users/search/', app_lease.api.user_search, name='user_search'),
    path('user/<int:pk>', app_lease.api.user_edit, name='user_edit'),
    path('user/', app_lease.api.user_add, name='user_add'),

    # ----- API Customer
    path('customers/', app_lease.api.customer_list, name='customers'),
    path('customer/<int:pk>', app_lease.api.customer_edit, name='customer_edit'),
    path('customers/search/', app_lease.api.customer_search, name='customer_search'),
    #path('customers/<int:pk>', api.CustomerDetail.as_view()),

    # ----- API Vehicle
    path('vehicles/', app_lease.api.vehicle_list, name='vehicles'),
    path('vehicle/<int:pk>', app_lease.api.vehicle_edit, name='vehicle_edit'),
    path('vehicles_for_customer/<int:pk>', app_lease.api.vehicles_for_customer, name='vehicles_for_customer'),
    path('vehicles/search/', app_lease.api.vehicle_search, name='vehicle_search'),

    # ----- API Lead
    path('leads/', app_lease.api.lead_list, name='leads'),
    path('lead/<int:pk>', app_lease.api.lead_edit, name='lead_edit'),
    path('leads/search/', app_lease.api.lead_search, name='lead_search'),

    # ----- API Services
    path('services/', app_lease.api.service_list, name='services'),
    path('service/<int:pk>', app_lease.api.service_edit, name='service_edit'),
    path('services/search/', app_lease.api.service_search, name='service_search'),

    # ----- API Credit Card
    path('credit_cards/', app_lease.api.credit_card_list, name='credit_cards'),
    path('credit_card/<int:pk>', app_lease.api.credit_card_edit, name='credit_card_edit'),
    path('credit_cards_for_customer/<int:pk>', app_lease.api.credit_cards_for_customer, name='credit_cards_for_customer'),
    path('credit_cards/search/', app_lease.api.credit_card_search, name='credit_card_search'),

    # ----- API Contact
    path('contact/', app_lease.api.contact_list, name='contacts'),
    path('contact/<int:pk>', app_lease.api.contact_edit, name='contact_edit'),
    path('contacts_for_customer/<int:pk>', app_lease.api.contacts_for_customer, name='contacts_for_customer'),
    path('contacts_for_lead/<int:pk>', app_lease.api.contacts_for_lead, name='contacts_for_lead'),
    path('contacts/search/', app_lease.api.contact_search, name='contact_search'),

    # ----- API Contact
    path('trades/', api.TradeList.as_view()),
    path('trades/<int:pk>', api.TradeDetail.as_view()),

    # ----- View Sets
    path('', include(router.urls)),
]
