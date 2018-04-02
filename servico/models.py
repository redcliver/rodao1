from django.db import models

# Create your models here.
class servico(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=200)
    valor = models.DecimalField(max_digits=6, decimal_places=2)
    
    def __str__(self):
        return self.nome