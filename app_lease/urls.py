from django.urls import path, include
from app_lease import api
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

router = routers.DefaultRouter()
router.register(r'users', api.UserViewSet)
router.register(r'groups', api.GroupViewSet)


urlpatterns = [
    path('services/', api.service_list),
    path('services/<int:pk>', api.service_detail),
    path('customers/', api.CustomerList.as_view()),
    path('customers/<int:pk>', api.CustomerDetail.as_view()),
    path('lead/', api.LeadList.as_view()),
    path('leads/<int:pk>', api.LeadDetail.as_view()),
    path('vehicles/', api.VehicleList.as_view()),
    path('vehicles/<int:pk>', api.VehicleDetail.as_view()),
    path('trades/', api.TradeList.as_view()),
    path('trades/<int:pk>', api.TradeDetail.as_view()),

    path('register/', api.user.user_api.user_register, name='api_register'),
    path('login/', obtain_auth_token),



    path('', include(router.urls)),
]
