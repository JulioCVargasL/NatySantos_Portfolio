from django.db import models
from django.utils.text import slugify

# Gestion de portafolio fotografico/Galerias 

class PortfolioCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    display_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        verbose_name = "Categoría de Portafolio"
        verbose_name_plural = "Categorías de Portafolio"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.display_name

class Portfolio(models.Model):
  title = models.CharField(max_length=100)
  description = models.TextField(blank=True)
  category = models.ForeignKey(PortfolioCategory, on_delete=models.CASCADE, related_name='portfolios')

  def __str__(self):
    return self.title
  
class photo(models.Model):
  portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='photos')
  image = models.ImageField(upload_to='static/img/webp_format/')
  order = models.PositiveIntegerField(default=0)

  def __str__(self):
    return f"Foto de {self.portfolio.title} (#{self.order})"
  
  
# Gestion de clientes y sesiones fotograficas

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    ID_CC = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.nombre
    
class TipoEvento(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class EstadoEvento(models.Model):
    estado = models.CharField(max_length=100)

    def __str__(self):
        return self.estado

class Evento(models.Model):
    tipoEvento = models.ForeignKey(TipoEvento, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    estado = models.ForeignKey(EstadoEvento, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    ubicacion = models.CharField(max_length=200)
    fecha_evento = models.DateField()
    fecha_reserva = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.titulo} - {self.fecha_evento}"
