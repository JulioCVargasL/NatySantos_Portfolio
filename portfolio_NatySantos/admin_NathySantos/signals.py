from django.db.models.signals import post_save, post_delete,pre_save
from django.core.exceptions import ObjectDoesNotExist
from django.dispatch import receiver
from django.conf import settings
import os
import shutil

from .models import PortfolioCategory

#Creacion de Portafolio

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

#Eliminacion de portafolio

@receiver(post_delete, sender=PortfolioCategory)
def delete_portfolio_template_and_folder(sender, instance, **kwargs):
    # Borrar carpeta de imágenes
    images_dir = os.path.join(settings.BASE_DIR, 'static', 'img', 'webp_format', instance.slug)
    if os.path.exists(images_dir):
        shutil.rmtree(images_dir)
        print(f"🗑 Carpeta eliminada: {images_dir}")

    # Borrar plantilla HTML
    template_path = os.path.join(settings.BASE_DIR, 'templates', 'portfolio', f"{instance.slug}.html")
    if os.path.exists(template_path):
        os.remove(template_path)
        print(f"🗑 Plantilla eliminada: {template_path}")

# Edicion de portafolio

@receiver(pre_save, sender=PortfolioCategory)
def rename_portfolio_assets_if_slug_changed(sender, instance, **kwargs):
    try:
        old_instance = PortfolioCategory.objects.get(pk=instance.pk)
    except ObjectDoesNotExist:
        return  # Es nuevo, no hay nada que renombrar

    old_slug = old_instance.slug
    new_slug = instance.slug

    if old_slug != new_slug:
        # Renombrar carpeta
        old_images_dir = os.path.join(settings.BASE_DIR, 'static', 'img', 'webp_format', old_slug)
        new_images_dir = os.path.join(settings.BASE_DIR, 'static', 'img', 'webp_format', new_slug)

        if os.path.exists(old_images_dir):
            os.rename(old_images_dir, new_images_dir)
            print(f"📂 Carpeta renombrada: {old_slug} -> {new_slug}")

        # Renombrar HTML
        template_dir = os.path.join(settings.BASE_DIR, 'templates', 'portfolio')
        old_template_path = os.path.join(template_dir, f"{old_slug}.html")
        new_template_path = os.path.join(template_dir, f"{new_slug}.html")

        if os.path.exists(old_template_path):
            os.rename(old_template_path, new_template_path)
            print(f"📝 HTML renombrado: {old_slug}.html -> {new_slug}.html")