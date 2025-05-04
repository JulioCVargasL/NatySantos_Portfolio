from django.db import models

# Create your models here.

class PortfolioCategory(models.Model):
  name = models.CharField(max_length=50, unique=True)
  display_name = models.CharField(max_length=100)

  class Meta:
    vervose_name = "Catergoria de Portafolio"
    vervose_name_plural = "Categorías de Portafolio"

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