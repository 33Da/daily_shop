from django.urls import path
from df_cart import views

urlpatterns = [
    path('cart/',views.cart),
    # 添加物品url
    path('cart_<int:gid>_<int:count>/',views.add),
    path('cart/edit<int:cart_id>_<int:count>/',views.edit),
    path('cart/del<int:cart_id>/',views.delete),

]