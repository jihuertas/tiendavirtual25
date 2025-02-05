from django.contrib import admin
from django.urls import path, include
from .views import *


urlpatterns = [
    path('productos/crear', CrearProductos.as_view(), name='crear'),
    path('productos/listado', ListadoProductos.as_view(), name='listado'),
    path('productos/<int:pk>', DetalleProducto.as_view(), name='producto_detalle'),
    path('productos/<int:pk>/edit', EditarProducto.as_view(), name='producto_editar'),
    path('productos/<int:pk>/del', BorrarProducto.as_view(), name='producto_borrar'),
    path('', ComprarProducto.as_view(), name='compra_listado'),
    path('checkout/<int:pk>',Checkout.as_view(),name='checkout'),
    path('informes',informes,name='informes'),

]