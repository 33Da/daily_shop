from django.urls import path
from df_order.views import *
urlpatterns = [
    path('order/',order),
    path('order/order_handle/',order_handle),
]