from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import PortfolioCategoryForm

# Create your views here.

@login_required

def create_category(request):
  if request.method == 'POST':
    form = PortfolioCategoryForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect('menuPortfolio')
    
  else:
    form = PortfolioCategoryForm()
  
  return render(request, 'admin_NathySantos/create_category.html', {'form': form})