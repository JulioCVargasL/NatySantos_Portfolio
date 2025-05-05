from django import forms
from .models import PortfolioCategory

class PortfolioCategoryForm(forms.ModelForm):
  class Meta:
    model = PortfolioCategory
    fields = ['display_name','slug']
    