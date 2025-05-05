from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
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

# Calendario

def calendar (request):
  return render(request,'calendar.html')

# Contacto

def contact (request):
  if request.method == 'POST':
    nombre = request.POST.get('nombre')
    correo = request.POST.get('correo')
    telefono = request.POST.get('telefono')
    mensaje = request.POST.get('mensaje')

    contenido = f"Nombre: {nombre}\nCorreo: {correo}\nTeléfono: {telefono}\n\nMensaje{mensaje}"

    send_mail(
      subject="Nuevo mensaje de contacto - Nathy Santos WEB",
      message=contenido,
      from_email='tuemail@gmail.com',
      recipient_list=['nathysantosfotografia@gmail.com'],
      fail_silently=False,
    )
    return redirect(request, 'contact')
  return render(request, 'contact.html')

def portfolio_dynamic_view(request, category_slug):
  folder_path = os.path.join(settings.BASE_DIR, 'static', 'img', 'webp_format', category_slug)

  if not os.path.exists(folder_path):
    raise Http404("Categoria no encontrada")

  filenames = [f for f in os.listdir(folder_path) if f.endswith('.webp')]
  filenames.sort()

  template_path = f'portfolio/{category_slug}.html'
  return render(request, template_path, {'images': filenames})