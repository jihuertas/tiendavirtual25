from django import forms
from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

class UsuarioCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name')

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Correo Electrónico'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Contraseña'
        })
    )

class CompraForm(forms.Form):
    unidades = forms.IntegerField(min_value=1)
    cod_descuento = forms.CharField(max_length=10, required=False)

