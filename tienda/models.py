from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Usuario(AbstractUser):

    vip = models.BooleanField(default=False)
    saldo = models.DecimalField(decimal_places=2, max_digits=12, default=0.00)

    def __str__(self):
        return f'{self.username}'

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
class Marca(models.Model):
    nombre = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return f'{self.nombre}'
    
    class Meta:
        verbose_name = "Marca"
        verbose_name_plural = "Marcas" 
class Producto(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    marca = models.ForeignKey("Marca", on_delete=models.CASCADE)
    modelo = models.CharField(max_length=50)
    unidades = models.IntegerField()
    precio = models.DecimalField(decimal_places=2, max_digits=12, default=0.00)
    vip = models.BooleanField(default=False)
    foto = models.ImageField(upload_to='productos/', null=True, blank=True)

    def __str__(self):
        return f'{self.nombre}'
    
    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
    

        



    