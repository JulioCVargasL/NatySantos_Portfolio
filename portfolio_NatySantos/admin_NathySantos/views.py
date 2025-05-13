from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.http import JsonResponse,HttpResponseRedirect
from django.conf import settings
from django.urls import reverse
from calendar import month_name
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
@login_required(login_url='/login/')
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
@login_required(login_url='/login/')
def cliente_create(request):
    if request.method == "POST":
        print("Se envió el formulario")
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("clientes_list")
        else:
            print("Errores del formulario:", form.errors) 
    return redirect("clientes_list")

@login_required(login_url='/login/')
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
@login_required(login_url='/login/')
def cliente_delete(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == "POST":
        cliente.delete()
        return redirect("clientes_list")
    return render(request, "/eliminar_cliente.html", {"cliente": cliente})

#Gestion de Sesiones
@login_required(login_url='/login/')
def crear_evento(request, cliente_id):
    cliente = get_object_or_404(Cliente, pk=cliente_id)
    tipo_eventos = TipoEvento.objects.all()
    eventos = Evento.objects.filter(cliente=cliente).order_by('-fecha_evento')

    estado_default = EstadoEvento.objects.filter(estado="Pendiente").first()
    if not estado_default:
      estado_default  = EstadoEvento.objects.create(estado="Pendiente")

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

        return redirect('crear_evento', cliente_id=cliente.id)

    return render(request, 'clientes/sesiones.html', {
        'cliente': cliente,
        'tipo_eventos': tipo_eventos,
        'eventos': eventos,
    })

# Tipos de eventos
@login_required(login_url='/login/')
def tipo_evento_create(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        if nombre:
            TipoEvento.objects.create(nombre=nombre)
    return redirect(request.META.get('HTTP_REFERER', 'clientes_list'))

#API creasion de tipos de eventos
@login_required(login_url='/login/')
def api_tipo_eventos(request):
    tipos = TipoEvento.objects.all().values('id', 'nombre')
    return JsonResponse(list(tipos), safe=False)

@csrf_exempt
def delete_tipo_evento(request, pk):
    if request.method == 'POST':
        TipoEvento.objects.filter(pk=pk).delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)

# CRUD Eventos
@login_required(login_url='/login/')
def editar_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    tipo_eventos = TipoEvento.objects.all()
    estados = EstadoEvento.objects.all()

    if request.method == 'POST':
        evento.tipoEvento_id = request.POST.get('tipo_evento')
        evento.estado_id = request.POST.get('estado')
        evento.fecha_evento = request.POST.get('fecha_evento')
        evento.descripcion = request.POST.get('descripcion')
        evento.ubicacion = request.POST.get('ubicacion')
        evento.save()
        return redirect('crear_evento', cliente_id=evento.cliente.pk)

    return render(request, 'clientes/editar_evento.html', {
        'evento': evento,
        'tipo_eventos': tipo_eventos,
        'estados': estados,
    })

@login_required(login_url='/login/')
def eliminar_evento(request, pk):
    
    evento = get_object_or_404(Evento, pk=pk)
    cliente_id = evento.cliente.pk
    if request.method == 'POST':
        evento.delete()
    return redirect('crear_evento', cliente_id=cliente_id)

@login_required(login_url='/login/')
def listar_eventos(request):
    estados_eventos()
    query = request.GET.get('q', '').strip()
    tipo = request.GET.get('tipo', '')
    mes = request.GET.get('mes', '')

    eventos = Evento.objects.select_related('cliente', 'tipoEvento', 'estado')

    if query:
        eventos = eventos.filter(
            Q(cliente__nombre__icontains=query) |
            Q(cliente__ID_CC__icontains=query)
        )

    if tipo:
        eventos = eventos.filter(tipoEvento_id=tipo)

    if mes:
        eventos = eventos.filter(fecha_evento__month=mes)

    eventos = eventos.order_by('-fecha_evento')

    tipos = TipoEvento.objects.all()

    return render(request, 'admin_NathySantos/lista_eventos.html', {
        'eventos': eventos,
        'tipos': tipos,
        'meses': meses,
        'query': query,
        'mes': mes,
        'tipo': tipo,
    })

# Lista de meses
meses = [(i, month_name[i]) for i in range(1, 13)]

# Estados de los eventos
def estados_eventos():
    from .models import EstadoEvento

    estados = [
        "pendiente",
        "pago_parcial",
        "pago_completo",
        "cancelado"
    ]

    for e in estados:
        EstadoEvento.objects.get_or_create(estado=e)


    