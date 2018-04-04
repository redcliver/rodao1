from ordem.printing import MyPrint
from io import BytesIO
from django.shortcuts import render
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.contrib.auth import authenticate
from decimal import *
from cliente.models import cliente
from servico.models import servico
from produto.models import produto
from funcionario.models import funcionario
from ordem.models import ordens, servico_item, produto_item
from caixa.models import caixa_geral
from datetime import datetime

# Create your views here.
def ordem(request):
    if request.user.is_authenticated():
        clientes = cliente.objects.all()
        servicos = servico.objects.all()
        produtos = produto.objects.all()
        funcionarios = funcionario.objects.all()
        hoje = datetime.now()
        return render(request, 'ordem.html', {'title':'Ordem', 'clientes':clientes, 'servicos':servicos, 'produtos':produtos,'funcionarios':funcionarios, 'hoje':hoje})
    else:
        return render(request, 'erro.html', {'title':'Erro'})

def busca(request):
    if request.user.is_authenticated():
        clientes = cliente.objects.all()
        if request.method == 'POST' and request.POST.get('cliente_id') != None:
            cliente_id = request.POST.get('cliente_id')
            ordens_cliente = ordens.objects.filter(cliente_ordem__id=cliente_id).all()
            return render(request, 'busca_ordem.html', {'title':'Busca Ordens', 'clientes':clientes, 'ordens_cliente':ordens_cliente})
        return render(request, 'busca_ordem.html', {'title':'Busca Ordens', 'clientes':clientes})
    else:
        return render(request, 'erro.html', {'title':'Erro'})

def abrir(request):
    if request.user.is_authenticated():
        if request.method == 'POST' and request.POST.get('cliente_id') != None and request.POST.get('servico_id') == None and request.POST.get('produto_id') == None:
            cliente_id = request.POST.get('cliente_id')
            cliente_obj = cliente.objects.filter(id=cliente_id).get()
            ordem_obj = ordens(cliente_ordem=cliente_obj, estado=1, total="0")
            ordem_obj.save()
            produtos1 = ordem_obj.prod_item.all()
            servicos1 = ordem_obj.serv_item.all()
            servicos = servico.objects.all()
            produtos = produto.objects.all()
            funcionarios = funcionario.objects.all()
            return render(request, 'edit_ordem.html', {'title':'Abrir Ordem', 'ordem_obj':ordem_obj, 'produtos1':produtos1, 'servicos1':servicos1, 'produtos':produtos, 'servicos':servicos, 'cliente_id':cliente_id, 'funcionarios':funcionarios})
        elif request.method == 'POST' and request.POST.get('cliente_id') != None and request.POST.get('servico_id') != None and request.POST.get('funcionario_id') != None and request.POST.get('produto_id') == None:
            cliente_id = request.POST.get('cliente_id')
            servico_id = request.POST.get('servico_id')
            qnt_servico = request.POST.get('qnt_servico')
            func_id = request.POST.get('funcionario_id')
            cliente_obj = cliente.objects.filter(id=cliente_id).get()
            servico_obj = servico.objects.filter(id=servico_id).get()
            func_obj = funcionario.objects.filter(id=func_id).get()
            total_serv = servico_obj.valor * Decimal(qnt_servico)
            novo_servico = servico_item(serv_item = servico_obj, quantidade = qnt_servico, total = total_serv, func = func_obj)
            novo_servico.save()
            ordem_obj = ordens(cliente_ordem=cliente_obj, estado=1, total="0")
            ordem_obj.save()
            ordem_obj.serv_item.add(novo_servico)
            ordem_obj.total = novo_servico.total
            ordem_obj.save()
            produtos1 = ordem_obj.prod_item.all()
            servicos1 = ordem_obj.serv_item.all()
            servicos = servico.objects.all()
            produtos = produto.objects.all()
            funcionarios = funcionario.objects.all()
            return render(request, 'edit_ordem.html', {'title':'Abrir Ordem', 'ordem_obj':ordem_obj, 'produtos1':produtos1, 'servicos1':servicos1, 'produtos':produtos, 'servicos':servicos, 'cliente_id':cliente_id, 'funcionarios':funcionarios})
        elif request.method == 'POST' and request.POST.get('cliente_id') != None and request.POST.get('servico_id') == None and request.POST.get('produto_id') != None:
            cliente_id = request.POST.get('cliente_id')
            produto_id = request.POST.get('produto_id')
            qnt_produto = request.POST.get('qnt_produto')
            cliente_obj = cliente.objects.filter(id=cliente_id).get()
            produto_obj = produto.objects.filter(id=produto_id).get()
            total_prod = produto_obj.valor_venda * Decimal(qnt_produto)
            novo_produto = produto_item(prod_item = produto_obj, quantidade = qnt_produto, total = total_prod)
            novo_produto.save()
            ordem_obj = ordens(cliente_ordem=cliente_obj, estado=1, total="0")
            ordem_obj.save()
            ordem_obj.prod_item.add(novo_produto)
            ordem_obj.total = novo_produto.total
            ordem_obj.save()
            produtos1 = ordem_obj.prod_item.all()
            servicos1 = ordem_obj.serv_item.all()
            servicos = servico.objects.all()
            produtos = produto.objects.all()
            funcionarios = funcionario.objects.all()
            return render(request, 'edit_ordem.html', {'title':'Abrir Ordem', 'ordem_obj':ordem_obj, 'produtos1':produtos1, 'servicos1':servicos1, 'produtos':produtos, 'servicos':servicos, 'cliente_id':cliente_id, 'funcionarios':funcionarios})
        elif request.method == 'POST' and request.POST.get('cliente_id') != None and request.POST.get('servico_id') != None and request.POST.get('produto_id') != None:
            cliente_id = request.POST.get('cliente_id')
            produto_id = request.POST.get('produto_id')
            servico_id = request.POST.get('servico_id')
            qnt_produto = request.POST.get('qnt_produto')
            qnt_servico = request.POST.get('qnt_servico')
            func_id = request.POST.get('funcionario_id')
            cliente_obj = cliente.objects.filter(id=cliente_id).get()
            servico_obj = servico.objects.filter(id=servico_id).get()
            total_serv = servico_obj.valor * Decimal(qnt_servico)
            func_obj = funcionario.objects.filter(id=func_id).get()
            novo_servico = servico_item(serv_item = servico_obj, quantidade = qnt_servico, func = func_obj)
            novo_servico.total = total_serv
            novo_servico.save()
            produto_obj = produto.objects.filter(id=produto_id).get()
            total_prod = produto_obj.valor_venda * Decimal(qnt_produto)
            novo_produto = produto_item(prod_item = produto_obj, quantidade = qnt_produto, total = total_prod)
            novo_produto.save()
            ordem_obj = ordens(cliente_ordem=cliente_obj, estado=1, total="0")
            ordem_obj.save()
            ordem_obj.prod_item.add(novo_produto)
            ordem_obj.serv_item.add(novo_servico)
            ordem_obj.total = novo_servico.total + novo_produto.total
            ordem_obj.save()
            produtos1 = ordem_obj.prod_item.all()
            servicos1 = ordem_obj.serv_item.all()
            servicos = servico.objects.all()
            produtos = produto.objects.all()
            funcionarios = funcionario.objects.all()
            return render(request, 'edit_ordem.html', {'title':'Abrir Ordem', 'ordem_obj':ordem_obj, 'produtos1':produtos1, 'servicos1':servicos1, 'produtos':produtos, 'servicos':servicos, 'cliente_id':cliente_id, 'funcionarios':funcionarios})
    else:
        return render(request, 'erro.html', {'title':'Erro'})

def editar(request):
    if request.user.is_authenticated():
       if request.method == 'POST' and request.POST.get('ordem_id') != None :
            ordem_id = request.POST.get('ordem_id')
            cliente_id = request.POST.get('cliente_id')
            ordem_obj = ordens.objects.filter(id = ordem_id).get()
            produtos1 = ordem_obj.prod_item.all()
            servicos1 = ordem_obj.serv_item.all()
            servicos = servico.objects.all()
            produtos = produto.objects.all()
            funcionarios = funcionario.objects.all()
            return render(request, 'edit_ordem.html', {'title':'Editar Ordens', 'ordem_obj':ordem_obj, 'produtos1':produtos1, 'servicos1':servicos1, 'produtos':produtos, 'servicos':servicos, 'cliente_id':cliente_id, 'funcionarios':funcionarios})
           
    else:
        return render(request, 'erro.html', {'title':'Erro'})

def fechar(request):
    if request.user.is_authenticated():
        clientes = cliente.objects.all()
        ordens1 = ordens.objects.filter(estado=1).all()
        if request.method == 'POST' and request.POST.get('ordem_id') != None:
            ordem_id = request.POST.get('ordem_id')
            ordem_obj = ordens.objects.filter(id = ordem_id).get()
            caixa = caixa_geral.objects.latest('id')
            total = caixa.total + ordem_obj.total
            desc = "Ordem numero "+str(ordem_id)+"."
            novo_caixa = caixa_geral(tipo=1, total=total, desc=desc)
            novo_caixa.save()
            ordem_obj.estado = 2
            ordem_obj.save()
            msg = "Ordem finalizada com sucesso"
            return render(request, 'home/index.html', {'title':'Home', 'msg':msg})
        return render(request, 'fechar_ordem.html', {'title':'Fechar Ordens', 'clientes':clientes, 'ordens1':ordens1})
    else:
        return render(request, 'erro.html', {'title':'Erro'})

def add_serv(request):
    if request.user.is_authenticated():
        clientes = cliente.objects.all()
        if request.method == 'POST' and request.POST.get('servico_id') != None and request.POST.get('produto_id') == None:
            ordem_id = request.POST.get('ordem_id')
            cliente_id = request.POST.get('cliente_id')
            servico_id = request.POST.get('servico_id')
            qnt_servico = request.POST.get('qnt_servico')
            func_id = request.POST.get('funcionario_id')
            cliente_obj = cliente.objects.filter(id=cliente_id).get()
            servico_obj = servico.objects.filter(id=servico_id).get()
            func_obj = funcionario.objects.filter(id=func_id).get()
            total_serv = servico_obj.valor * Decimal(qnt_servico)
            novo_servico = servico_item(serv_item = servico_obj, quantidade = qnt_servico, total = total_serv, func = func_obj)
            novo_servico.save()
            ordem_obj = ordens.objects.filter(id=ordem_id).get()
            ordem_obj.serv_item.add(novo_servico)
            ordem_obj.total = ordem_obj.total + novo_servico.total
            ordem_obj.save()
            ordens_cliente = ordens.objects.filter(cliente_ordem__id=cliente_id, estado=2).all()
            produtos1 = ordem_obj.prod_item.all()
            servicos1 = ordem_obj.serv_item.all()
            servicos = servico.objects.all()
            produtos = produto.objects.all()
            funcionarios = funcionario.objects.all()
            return render(request, 'edit_ordem.html', {'title':'Abrir Ordem', 'ordem_obj':ordem_obj, 'produtos1':produtos1, 'servicos1':servicos1, 'produtos':produtos, 'servicos':servicos, 'cliente_id':cliente_id, 'funcionarios':funcionarios})
        return render(request, 'edit_ordem.html', {'title':'Editar Ordens', 'clientes':clientes})
    else:
        return render(request, 'erro.html', {'title':'Erro'})

def add_prod(request):
    if request.user.is_authenticated():
        clientes = cliente.objects.all()
        if request.method == 'POST' and request.POST.get('produto_id') != None and request.POST.get('servico_id') == None:
            ordem_id = request.POST.get('ordem_id')
            cliente_id = request.POST.get('cliente_id')
            produto_id = request.POST.get('produto_id')
            qnt_produto = request.POST.get('qnt_produto')
            cliente_obj = cliente.objects.filter(id=cliente_id).get()
            produto_obj = produto.objects.filter(id=produto_id).get()
            total_prod = produto_obj.valor_venda * Decimal(qnt_produto)
            novo_produto = produto_item(prod_item = produto_obj, quantidade = qnt_produto, total = total_prod)
            novo_produto.save()
            ordem_obj = ordens.objects.filter(id=ordem_id).get()
            ordem_obj.prod_item.add(novo_produto)
            ordem_obj.total = ordem_obj.total + novo_produto.total
            ordem_obj.save()
            ordens_cliente = ordens.objects.filter(cliente_ordem__id=cliente_id, estado=2).all()
            produtos1 = ordem_obj.prod_item.all()
            servicos1 = ordem_obj.serv_item.all()
            servicos = servico.objects.all()
            produtos = produto.objects.all()
            funcionarios = funcionario.objects.all()
            return render(request, 'edit_ordem.html', {'title':'Abrir Ordem', 'ordem_obj':ordem_obj, 'produtos1':produtos1, 'servicos1':servicos1, 'produtos':produtos, 'servicos':servicos, 'cliente_id':cliente_id, 'funcionarios':funcionarios})
        return render(request, 'edit_ordem.html', {'title':'Editar Ordens', 'clientes':clientes})
    else:
        return render(request, 'erro.html', {'title':'Erro'})
    
def imprimir(request):
    ordem_id = request.POST.get('ordem_id')
    ordem_obj = ordens.objects.filter(id=ordem_id).get()
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    cliente = str(ordem_obj.cliente_ordem)
    response['Content-Disposition'] = 'attachment; filename="'+cliente+'.pdf"'
 
    buffer = BytesIO()
 
    report = MyPrint(buffer, 'Letter')
    pdf = report.print_users(ordem_id)
 
    response.write(pdf)
    return response