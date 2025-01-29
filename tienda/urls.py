from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('admin/productos/listado', views.listado, name='listado'),
    path('admin/productos/', views.listado, name='listado'),
]