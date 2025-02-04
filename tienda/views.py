from django.shortcuts import get_object_or_404, render
from .models import *
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView,DeleteView
from django.urls import reverse_lazy
from .forms import CompraForm

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
    
    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        marcas = Marca.objects.filter(producto__isnull=False).distinct()
        contexto["marcas"] = marcas

        form = CompraForm()
        contexto['compra_form'] = form

        return contexto

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
    
class Checkout(View):
# seguir aquí



class CrearCompra(CreateView):
    model = Compra
    template_name = 'tienda/compra_crear.html'
    fields = ['unidades', 'usuario', 'importe', 'producto']
    success_url = reverse_lazy('compra_listado')

    def form_valid(self, form):
        producto = get_object_or_404(Producto, pk=self.kwargs['pk'])
        importe = 10
        form.instance.producto = producto

        print (producto)
        return super().form_valid(form)
    
