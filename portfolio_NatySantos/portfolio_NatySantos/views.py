from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

import os

from admin_NathySantos.models import PortfolioCategory
from django.http import Http404


#Pagina principal

def index (request):
  return render(request, 'index.html')

# ¿Quien soy?

def nathySantos (request):
  return render(request, 'nathySantos.html')

# Portafolios

def menuPortfolio (request):
  return render(request, 'portfolio/menuPortfolio.html')

# Portafolios / weddings

def weddings (request):
  folder_path = os.path.join(settings.BASE_DIR, 'static/img/webp_format/weddings')
  filenames = [f for f in os.listdir(folder_path) if f.endswith('.webp')]
  filenames.sort()
  return render(request, 'portfolio/weddings.html', {'images': filenames})

# Portafolios / 15 años

def yearsOld_15 (request):
  folder_path = os.path.join(settings.BASE_DIR, 'static/img/webp_format/15yearsOld')
  filenames = [f for f in os.listdir(folder_path) if f.endswith('.webp')]
  filenames.sort()
  return render(request, 'portfolio/15yearsOld.html', {'images': filenames})

# Portafolios / Eventos por tiempo

def timeEvents (request):
  folder_path = os.path.join(settings.BASE_DIR, 'static/img/webp_format/timeEvents')
  filenames = [f for f in os.listdir(folder_path) if f.endswith('.webp')]
  filenames.sort()
  return render(request, 'portfolio/timeEvents.html', {'images': filenames})

# Definir Menu Portafolio

def menuPortfolio(request):

    categorias = PortfolioCategory.objects.all()
    base_path = os.path.join(settings.BASE_DIR, 'static', 'img', 'webp_format')
    data = []

    for categoria in categorias:
        folder_path = os.path.join(base_path, categoria.slug)
        image = None
        if os.path.isdir(folder_path):
            for file in sorted(os.listdir(folder_path)):
                if file.endswith('.webp'):
                    image = f'img/webp_format/{categoria.slug}/{file}'
                    break
        data.append({
            'slug': categoria.slug,
            'name': categoria.name,
            'display_name': categoria.display_name,
            'image': image,
        })

    return render(request, 'portfolio/menuPortfolio.html', {'portfolios': data})

# Calendario

def calendar (request):
  return render(request,'calendar.html')

# Contacto

def contact(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        correo = request.POST.get('correo')
        telefono = request.POST.get('telefono')
        mensaje = request.POST.get('mensaje')

        contenido = (
            f"Nuevo mensaje desde el formulario de contacto\n\n"      
            f"Nombre: {nombre}\n\n"
            f"Correo: {correo}\n"
            f"Teléfono: {telefono}\n\n"
            f"Mensaje:\n{mensaje}"
        )

        send_mail(
            subject="Nuevo mensaje de contacto - Nathy Santos WEB",
            message=contenido,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['nathysantosfotografia@gmail.com'],
            fail_silently=False,
        )

        enviados = send_mail(
            subject=f"{nombre} te envio un mensaje - Nathy Santos WEB",
            message=contenido,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['nathysantosfotografia@gmail.com'],
            fail_silently=False,
        )

        print("Correos enviados:", enviados)

        messages.success(request, "Tu mensaje fue enviado exitosamente.")
        return redirect('contact')

    return render(request, 'contact.html')

# Portafolios dinámicos

def portfolio_dynamic_view(request, category_slug):
  folder_path = os.path.join(settings.BASE_DIR, 'static', 'img', 'webp_format', category_slug)

  if not os.path.exists(folder_path):
    raise Http404("Categoria no encontrada")

  filenames = [f for f in os.listdir(folder_path) if f.endswith('.webp')]
  filenames.sort()

  try:
      category = PortfolioCategory.objects.get(slug=category_slug)
  except PortfolioCategory.DoesNotExist:
      raise Http404("Categoría no encontrada")

  template_path = f'portfolio/{category_slug}.html'
  return render(request, template_path, {
    'images': filenames,
    'category_display_name': category.display_name,
    'category_slug': category.slug
    })
    

