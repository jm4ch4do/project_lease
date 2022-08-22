from django.urls import path, include

import app_lease.api.user_api
from app_lease import api
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', api.UserViewSet)
router.register(r'groups', api.GroupViewSet)


urlpatterns = [
    path('services/', api.service_list),
    path('services/<int:pk>', api.service_detail),
    path('lead/', api.LeadList.as_view()),
    path('leads/<int:pk>', api.LeadDetail.as_view()),
    path('trades/', api.TradeList.as_view()),
    path('trades/<int:pk>', api.TradeDetail.as_view()),

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
    path('vehicles/search/', app_lease.api.vehicle_search, name='vehicle_search'),

    # ----- View Sets
    path('', include(router.urls)),
]
