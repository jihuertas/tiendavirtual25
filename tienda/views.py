from decimal import Decimal
from django.shortcuts import render
from .models import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView,DeleteView, View
from django.urls import reverse_lazy
from django.views.generic.edit import FormMixin
from .forms import CompraForm, CustomLoginForm, UsuarioCreationForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count


# Create your views here.

class ListadoProductos (LoginRequiredMixin, ListView):
    model = Producto
    template_name = 'tienda/productos_listado.html'
    # context_object_name = 'listaProductos'

class DetalleProducto (LoginRequiredMixin, DetailView):
    model = Producto
    template_name = 'tienda/producto_detalle.html'

class EditarProducto (LoginRequiredMixin, UpdateView):
    model = Producto
    template_name = 'tienda/producto_editar.html'
    fields = '__all__'
    success_url = reverse_lazy("listado")

class BorrarProducto (LoginRequiredMixin, DeleteView):
    model = Producto
    success_url = reverse_lazy("listado")

class CrearProductos(LoginRequiredMixin, CreateView):
    model = Producto
    template_name = 'tienda/producto_crear.html'
    fields = '__all__'
    success_url = reverse_lazy("listado")

class ComprarProducto (LoginRequiredMixin, ListView):
    model = Producto
    template_name = 'tienda/compra_listado.html'
    context_object_name = 'productos'
    paginate_by = 3
    
    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        marcas = Marca.objects.filter(producto__isnull = False).distinct
        contexto["marcas"] = marcas
        compraform = CompraForm()
        contexto['compra_form']= compraform
        return contexto

    def get_queryset(self):
        query = super().get_queryset()
        filtro_nombre = self.request.GET.get("filtro_nombre")
        filtro_marca = self.request.GET.get("filtro_marca")
        filtro_precio_max = self.request.GET.get("filtro_precio")

        if filtro_nombre :
            query = query.filter(nombre__icontains = filtro_nombre) 
        if filtro_marca:
            query = query.filter(marca__nombre = filtro_marca)
        if filtro_precio_max:
            query = query.filter(precio__lte = filtro_precio_max)
    
        return query
    
class CheckoutView(LoginRequiredMixin, View):
    
    def get(self, request, pk):
        producto = get_object_or_404(Producto, pk=pk)
        unidades = request.GET.get('unidades')
        cod_descuento = request.GET.get('cod_descuento')
        descuento = 0
        if cod_descuento:
             promocion = get_object_or_404(Promocion, codigo=cod_descuento)
             descuento = promocion.descuento
        total = producto.precio * int(unidades) * Decimal((100 - int(descuento))/100)
        form = CompraForm({'unidades': unidades, 'cod_descuento': cod_descuento})
        return render(request,'tienda/checkout.html', {'producto': producto,
                                                   'total': total,
                                                   'form': form, 'descuento':descuento})
    
    def post(self, request, pk):
        producto = get_object_or_404(Producto, pk=pk)
        total=0
        form = CompraForm(request.POST)

        if form.is_valid():
            unidades = form.cleaned_data['unidades']
            if unidades <= producto.unidades:
                client = request.user
                
                importetotal = unidades * producto.precio
                #importetotal = unidades * (producto.importe + (producto.importe * producto.iva))
                if client.saldo >= importetotal:
                    producto.unidades -= unidades
                    producto.save()
                    compra = Compra()
                    compra.producto = producto
                    compra.usuario = client
                    compra.unidades = unidades
                    compra.importe = unidades * producto.precio
                    #compra.fecha = datetime.datetime.now()
                    compra.save()
                    client.saldo -= compra.importe
                    client.save()
                    messages.info(request, "Compra realizada")
                else:
                    messages.error(request,"No tienes saldo sufiente")

            else:
                messages.error(request,"No existen unidades disponibles")
            return redirect('compra_listado')

        else:
            return render (request,'tienda/checkout.html', {'producto': producto, 'form': form} )
  

class RegistroView(CreateView):
    form_class = UsuarioCreationForm
    template_name = 'registration/registro.html'
    success_url = reverse_lazy('login')
    
@login_required
def informes(request):
    top10clientes = Usuario.objects.annotate(importe_compras = Sum('compra__importe'), total_compras = Count('compra')).order_by('-importe_compras')[:10]
    top10productos = Producto.objects.annotate(total_vendidos = Sum('compra__unidades')).order_by('-total_vendidos')[:10]
    return render(request, 'tienda/informes.html', {'top10clientes':top10clientes,'top10productos':top10productos})