from django.contrib import admin
from ordem.models import ordens
from cliente.models import cliente
from contas.models import conta
from funcionario.models import funcionario
from caixa.models import caixa_geral
from produto.models import produto
from servico.models import servico

admin.site.register(ordens)
admin.site.register(cliente)
admin.site.register(conta)
admin.site.register(funcionario)
admin.site.register(caixa_geral)
admin.site.register(produto)
admin.site.register(servico)