from django.shortcuts import render
from .models import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView,DeleteView
from django.urls import reverse_lazy

# Create your views here.

class ListadoProductos (ListView):
    model = Producto
    template_name = 'tienda/productos_listado.html'
    # context_object_name = 'listaProductos'

class DetalleProducto (DetailView):
    model = Producto
    template_name = 'tienda/producto_detalle.html'

class EditarProducto (UpdateView):
    model = Producto
    template_name = 'tienda/producto_editar.html'
    fields = '__all__'
    success_url = reverse_lazy("listado")

class BorrarProducto (DeleteView):
    model = Producto
    success_url = reverse_lazy("listado")

class CrearProductos(CreateView):
    model = Producto
    template_name = 'tienda/producto_editar.html'
    fields = '__all__'
    success_url = reverse_lazy("listado")