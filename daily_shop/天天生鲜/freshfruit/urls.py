from django.contrib import admin
from django.urls import path, include
from freshfruit import views
from django.conf.urls import url


urlpatterns = [
    path('register/', views.register),
    path('register_handle', views.register_handle),
    path('login/', views.login),
    path('user_site/', views.user_site),
    path('info/', views.info),
    path('login_handle', views.login_handle),
    path('register_username/',views.register_username),
    path('logout/',views.logout),
    path('order<int:pindex>/',views.order),




]