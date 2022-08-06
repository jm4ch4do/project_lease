from django.urls import path, include
from app_lease import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)


urlpatterns = [
    path('services/', views.service_list),
    path('services/<int:id>', views.service_detail),
    path('customers/', views.CustomerList.as_view()),
    path('customers/<int:pk>', views.CustomerDetail.as_view()),
    path('', include(router.urls)),
]
