from django.db import models
from django.utils import timezone

# Create your models here.
class caixa_geral(models.Model):
    TIPO = (
        ('1', 'Entrada'),
        ('2', 'Saida'),
    )
    id = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=1, choices=TIPO)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    desc = models.CharField(max_length=100)
    data = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.nome