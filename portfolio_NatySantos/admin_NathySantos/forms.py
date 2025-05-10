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