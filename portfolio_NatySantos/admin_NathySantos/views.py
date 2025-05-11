from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.http import JsonResponse
from django.conf import settings
from .models import PortfolioCategory, Cliente,Evento, TipoEvento, EstadoEvento
from .forms import PortfolioCategoryForm,ClienteForm
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
  query = request.GET.get("q", "").strip()

  if query:
      if query.isdigit():
          # Si es número, ordenamos por coincidencia de cédula
          clientes = Cliente.objects.filter(ID_CC__icontains=query).order_by('ID_CC')
      else:
          # Si es texto, ordenamos por coincidencia en nombre
          clientes = Cliente.objects.filter(nombre__icontains=query).order_by('nombre')
  else:
      # Sin búsqueda, mostrar ordenados por nombre
      clientes = Cliente.objects.all().order_by('nombre')

  return render(request, 'clientes/lista_clientes.html', {"clientes": clientes, "query": query})

#CRUD Clientes

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
    return render(request, "clientes/sesiones.html", {"form": form, "titulo": "Editar Cliente"})

def cliente_delete(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == "POST":
        cliente.delete()
        return redirect("clientes_list")
    return render(request, "/eliminar_cliente.html", {"cliente": cliente})

#Gestion de Sesiones

def crear_evento(request, cliente_id):
    cliente = get_object_or_404(Cliente, pk=cliente_id)
    tipo_eventos = TipoEvento.objects.all()
    estado_default = EstadoEvento.objects.first()  # Puedes ajustar esto si usas estados tipo "Pendiente"

    if request.method == 'POST':
        tipo_evento_id = request.POST.get('tipo_evento')
        fecha_evento = request.POST.get('fecha_evento')
        comentarios = request.POST.get('descripcion', '')
        
        tipo_evento = get_object_or_404(TipoEvento, pk=tipo_evento_id)

        Evento.objects.create(
            tipoEvento=tipo_evento,
            cliente=cliente,
            estado=estado_default,
            titulo=f"{tipo_evento.nombre} de {cliente.nombre}",
            descripcion=comentarios,
            ubicacion="",  # campo vacío por ahora
            fecha_evento=fecha_evento,
            fecha_reserva=fecha_evento
        )

        return redirect('clientes_list')

    return render(request, 'clientes/sesiones.html', {
        'cliente': cliente,
        'tipo_eventos': tipo_eventos
    })

# Tipos de eventos

def tipo_evento_create(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        if nombre:
            TipoEvento.objects.create(nombre=nombre)
    return redirect(request.META.get('HTTP_REFERER', 'clientes_list'))

#API creasion de eventos

def api_tipo_eventos(request):
    tipos = TipoEvento.objects.all().values('id', 'nombre')
    return JsonResponse(list(tipos), safe=False)

@csrf_exempt
def delete_tipo_evento(request, pk):
    if request.method == 'POST':
        TipoEvento.objects.filter(pk=pk).delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)