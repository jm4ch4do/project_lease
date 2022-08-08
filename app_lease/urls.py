from django.urls import path, include
from app_lease import apis
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', apis.UserViewSet)
router.register(r'groups', apis.GroupViewSet)


urlpatterns = [
    path('services/', apis.service_list),
    path('services/<int:pk>', apis.service_detail),
    path('customers/', apis.CustomerList.as_view()),
    path('customers/<int:pk>', apis.CustomerDetail.as_view()),
    path('lead/', apis.LeadList.as_view()),
    path('leads/<int:pk>', apis.LeadDetail.as_view()),
    path('vehicles/', apis.VehicleList.as_view()),
    path('vehicles/<int:pk>', apis.VehicleDetail.as_view()),
    path('trades/', apis.VehicleList.as_view()),
    path('trades/<int:pk>', apis.VehicleDetail.as_view()),
    path('', include(router.urls)),
]
