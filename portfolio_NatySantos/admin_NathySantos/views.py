from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import PortfolioCategory, Cliente
from django.db.models import Q
from .forms import PortfolioCategoryForm,ClienteForm
from django.conf import settings
import os

# Create your views here.

@login_required(login_url='/login/')
def dashboard(request):
    categorias = PortfolioCategory.objects.all()
    return render(request, 'admin_NathySantos/dashboard.html', {'categorias': categorias})

@login_required(login_url='/login/')
def create_category(request):
  if request.method == 'POST':
    form = PortfolioCategoryForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect('menuPortfolio')
    
  else:
    form = PortfolioCategoryForm()
  
  return render(request, 'admin_NathySantos/create_category.html', {'form': form})

# definicion CRUD panel-admin

@login_required(login_url='/login/')
def create_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        display_name = request.POST.get('display_name')
        slug = request.POST.get('slug')
        if display_name and slug:
            PortfolioCategory.objects.create(
               name=slug, 
               slug=slug,
               display_name=display_name,
               )
    return redirect('dashboard')


@login_required(login_url='/login/')
def edit_category(request, pk):
    categoria = get_object_or_404(PortfolioCategory, pk=pk)
    form = PortfolioCategoryForm(request.POST or None, instance=categoria)

    if request.method == 'POST' and form.is_valid():
        categoria = form.save(commit=False)
        categoria.name = categoria.slug
        categoria.save()
        return redirect('edit_category', pk=pk)

    return render(request, 'admin_NathySantos/category_form.html', {
        'form': form,
        'categoria': categoria,
        'form_title': f'Editar Categoría: {categoria.display_name}'
    })

@login_required(login_url='/login/')
def delete_category(request, pk):
    categoria = get_object_or_404(PortfolioCategory, pk=pk)
    categoria.delete()
    return redirect('dashboard')

@login_required(login_url='/login/')
def manage_category_images(request, pk):
    categoria = get_object_or_404(PortfolioCategory, pk=pk)
    folder_path = os.path.join(settings.BASE_DIR, 'static', 'img', 'webp_format', categoria.slug)
    os.makedirs(folder_path, exist_ok=True)

    if request.method == 'POST':
        if 'image_name' in request.POST:
            image_name = request.POST.get('image_name')
            image_path = os.path.join(folder_path, image_name)
            if os.path.exists(image_path):
                os.remove(image_path)
            return redirect('manage_images', pk=pk)

        if request.FILES.getlist('imagenes'):
            for img in request.FILES.getlist('imagenes'):
                if img.name.endswith('.webp'):
                    with open(os.path.join(folder_path, img.name), 'wb+') as f:
                        for chunk in img.chunks():
                            f.write(chunk)
            return redirect('manage_images', pk=pk)

    imagenes = []
    if os.path.isdir(folder_path):
        for archivo in sorted(os.listdir(folder_path)):
            if archivo.endswith('.webp'):
                imagenes.append({
                    'name': archivo,
                    'path': f'img/webp_format/{categoria.slug}/{archivo}'
                })

    return render(request, 'admin_NathySantos/manage_images.html', {
        'categoria': categoria,
        'imagenes': imagenes
    })

#Gestion de Clientes

def clientes_list(request):
    query = request.GET.get("q")
    clientes = Cliente.objects.filter(Q(nombre__icontains=query) | Q(ID_CC__icontains=query)) if query else Cliente.objects.all()
    return render(request, "lista_clientes.html", {"clientes": clientes, "query": query})

def cliente_create(request):
    if request.method == "POST":
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("clientes_list")
    else:
        form = ClienteForm()
    return render(request, "/form_cliente.html", {"form": form, "titulo": "Nuevo Cliente"})

def cliente_edit(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == "POST":
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect("clientes_list")
    else:
        form = ClienteForm(instance=cliente)
    return render(request, "/form_cliente.html", {"form": form, "titulo": "Editar Cliente"})

def cliente_delete(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == "POST":
        cliente.delete()
        return redirect("clientes_list")
    return render(request, "/eliminar_cliente.html", {"cliente": cliente})