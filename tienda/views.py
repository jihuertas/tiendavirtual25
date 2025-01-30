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
    template_name = 'tienda/producto_crear.html'
    fields = '__all__'
    success_url = reverse_lazy("listado")

class ComprarProducto (ListView):
    model = Producto
    template_name = 'tienda/compra_listado.html'
    context_object_name = 'productos'
    
    def get_queryset(self):

        query = super().get_queryset()
        filtro_nombre = self.request.GET.get("filtro_nombre")
        filtro_marca = self.request.GET.get("filtro_marca")
        filtro_precio_max = self.request.GET.get("filtro_precio")

        print(filtro_nombre)

        if filtro_nombre :
            query = query.filter(nombre__icontains = filtro_nombre)
        
        if filtro_marca:
            query = query.filter(marca__nombre = filtro_marca)

        if filtro_precio_max:
            query = query.filter(precio__lte = filtro_precio_max)
        


        return query
    