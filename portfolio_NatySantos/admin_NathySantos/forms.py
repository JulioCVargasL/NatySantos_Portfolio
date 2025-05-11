from django import forms
from .models import PortfolioCategory,Cliente

# Portafolios

class PortfolioCategoryForm(forms.ModelForm):
  class Meta:
    model = PortfolioCategory
    fields = ['display_name','slug']
    
# Gestion clientes

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'ID_CC', 'telefono', 'email']

# Gestion de Sesiones

from .models import SesionFotografica
from django import forms

class SesionFotograficaForm(forms.ModelForm):
    class Meta:
        model = SesionFotografica
        fields = ['nombre', 'fecha_sesion', 'galeria_url']