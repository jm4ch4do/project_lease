from .service_api import service_list, service_edit, service_search
from app_lease.api.user_api import UserViewSet
from .group_api import GroupViewSet
from .trade_api import TradeList, TradeDetail
from .user_api import *
from .customer_api import customer_list, customer_edit, customer_search
from .vehicle_api import vehicle_list, vehicle_edit, vehicle_search, vehicles_for_customer
from .lead_api import lead_list, lead_edit, lead_search
from .credit_card_api import credit_card_list, credit_card_edit, credit_card_search
from .contact_api import contact_list, contact_edit, contact_search,\
    contacts_for_customer, contacts_for_lead
