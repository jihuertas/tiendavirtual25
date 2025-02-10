from django.contrib import admin
from django.urls import path, include
from .views import *


urlpatterns = [
    path('productos/crear', CrearProductos.as_view(), name='producto_crear'),
    path('productos/listado', ListadoProductos.as_view(), name='listado'),
    path('productos/<int:pk>', DetalleProducto.as_view(), name='producto_detalle'),
    path('productos/<int:pk>/edit', EditarProducto.as_view(), name='producto_editar'),
    path('productos/<int:pk>/del', BorrarProducto.as_view(), name='producto_borrar'),

    path('', ComprarProducto.as_view(), name='compra_listado'),
    path('checkout/<int:pk>', CheckoutView.as_view(), name='checkout'),

    path('informes', informes, name='informes'),
    path('perfil', perfil.as_view(), name='perfil'),
    

    path('registro/', RegistroView.as_view(), name='registro'),
]