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

    # ----- API User
    path('register/', api.user.user_api.user_register, name='api_register'),
    path('password_update/<int:pk>', api.user.user_api.user_password_update,
         name='api_password_update'),
    path('login/', api.user.user_api.user_login, name='api_login'),
    path('users/', api.user.user_api.user_list, name='user_list'),
    path('users/search/', api.user.user_api.user_search, name='user_search'),
    path('user/', api.user.user_api.user_add, name='user_add'),


    # ----- View Sets
    path('', include(router.urls)),
]
