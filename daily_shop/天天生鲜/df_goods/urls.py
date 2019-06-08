from django.contrib import admin
from django.urls import path, include
from df_goods.views import *


from df_goods import views

urlpatterns = [
         path('',views.index),
         path('admin/', admin.site.urls),
         path('detail_<int:good_id>/',views.detail),
         path('list<int:type_id>_<int:pindex>_<int:sort>',views.list),



         path('search/', MySerchView()),



]
"""
     这里一定要用 from df_goods.views import *
     不能view.MySerchView()
      """