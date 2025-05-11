# admin_NathySantos/admin.py
from django.contrib import admin
from django.urls import path
from django.utils.html import format_html
from .models import PortfolioCategory,Cliente, Evento, TipoEvento, EstadoEvento
from .views import create_category

# Gestion de Portafolio

class PortfolioCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_name')
    change_list_template = "admin_NathySantos/category_changelist.html"  # Sobrescribe la plantilla

admin.site.register(PortfolioCategory, PortfolioCategoryAdmin)

# Gestion de clientes/Sesiones

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'ID_CC', 'telefono', 'email')
    search_fields = ('nombre', 'ID_CC')

@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'cliente', 'tipoEvento', 'estado', 'fecha_evento', 'fecha_reserva')
    list_filter = ('estado', 'tipoEvento')
    search_fields = ('titulo', 'cliente__nombre')

admin.site.register(TipoEvento)
admin.site.register(EstadoEvento)