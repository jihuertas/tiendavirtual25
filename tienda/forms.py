from django import forms

class CompraForm (forms.Form):
    unidades = forms.IntegerField(min_value=1)