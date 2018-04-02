from django.db import models
from django.utils import timezone
from cliente.models import cliente
from servico.models import servico
from produto.models import produto

# Create your models here.

class produto_item(models.Model):
    id = models.AutoField(primary_key=True)
    prod_item = models.ForeignKey(produto)
    quantidade = models.IntegerField(default='1')
    total = models.DecimalField(max_digits=6, decimal_places=2)

    def __int__(self):
        return self.id

class servico_item(models.Model):
    id = models.AutoField(primary_key=True)
    serv_item = models.ForeignKey(servico)
    quantidade = models.IntegerField(default='1')
    total = models.DecimalField(max_digits=6, decimal_places=2)

    def __int__(self):
        return self.id


class ordens(models.Model):
    ESTADO = (
        ('1', 'Orcamento'),
        ('2', 'Executando'),
        ('3', 'Finalizada'),
    )
    id = models.AutoField(primary_key=True)
    cliente_ordem = models.ForeignKey(cliente)
    prod_item = models.ManyToManyField(produto_item)
    serv_item = models.ManyToManyField(servico_item)
    estado = models.CharField(max_length=1, choices=ESTADO)
    data_abertura = models.DateTimeField(default=timezone.now)
    data_fechamento = models.DateTimeField(null=True, blank=True)
    desc = models.CharField(max_length=100, null=True, blank=True)
    total = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return str(self.id)