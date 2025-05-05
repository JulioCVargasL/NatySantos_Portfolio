# admin_NathySantos/admin.py
from django.contrib import admin
from django.urls import path
from django.utils.html import format_html
from .models import PortfolioCategory
from .views import create_category

class PortfolioCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_name')
    change_list_template = "admin_NathySantos/category_changelist.html"  # Sobrescribe la plantilla

admin.site.register(PortfolioCategory, PortfolioCategoryAdmin)
