from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
import os
import shutil

from .models import PortfolioCategory

@receiver(post_save, sender=PortfolioCategory)
def create_portfolio_template_and_folder(sender, instance, created, **kwargs):
  if created:
    # Crear carpeta de imagenes

    images_dir = os.path.join(settings.BASE_DIR, 'static','img','webp_format', instance.slug)
    os.makedirs(images_dir, exist_ok=True)

    # Crear Plantilla HTML

    template_dir = os.path.join(settings.BASE_DIR, 'templates','portfolio')
    new_template_path = os.path.join(template_dir, f"{instance.slug}.html")
    template_source_path = os.path.join(template_dir, "mainTemplate.html")

    # si ya existe

    if not os.path.exists(new_template_path):
      shutil.copy(template_source_path, new_template_path)

    else:
      print(f" ¡ El archivo {instance.slug}.html ya existe. No se sobreescribió. ! ")