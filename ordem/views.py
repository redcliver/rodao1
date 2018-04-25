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
from django.views.generic import View
from django.template.loader import get_template
from .utils import render_to_pdf
from django.utils import timezone
# Create your views here.

class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        template = get_template('pdf.html')
        os_id = request.GET.get('ordem_id')
        nome_orc = request.GET.get('nome_orc')
        ordem_obj = ordens.objects.filter(id=os_id).get()
        serv_obj = ordem_obj.serv_item.all()
        prod_obj = ordem_obj.prod_item.all()
        hoje = datetime.now().strftime('%d/%m/%Y')
        try:
            fechamento = ordem_obj.data_fechamento.strftime('%d/%m/%Y')
        except:
            fechamento = " "

        context = {
                "ordem_cli": ordem_obj.cliente_ordem,
                "ordem_id": ordem_obj.id,
                "ordem_abertura": ordem_obj.data_abertura.strftime('%d/%m/%Y'),
                "ordem_fechamento": fechamento,
                "ordem_nome": ordem_obj.cliente_ordem,
                "ordem": ordem_obj,
                "serv_obj": serv_obj,
                "prod_obj": prod_obj,
                "hoje": hoje,
                "nome_orc": nome_orc,
            }
        html = template.render(context)
        pdf = render_to_pdf('pdf.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "OS_%s.pdf" %(ordem_obj.cliente_ordem)
            content = "inline-block; filename='%s'" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")
        return HttpResponse(pdf, content_type='application/pdf')

def ordem(request):
    if request.user.is_authenticated():
        clientes = cliente.objects.all().order_by('nome')
        servicos = servico.objects.all().order_by('nome')
        produtos = produto.objects.all().order_by('nome')
        funcionarios = funcionario.objects.all().order_by('nome')
        hoje = datetime.now()
        return render(request, 'ordem.html', {'title':'Ordem', 'clientes':clientes, 'servicos':servicos, 'produtos':produtos,'funcionarios':funcionarios, 'hoje':hoje})
    else:
        return render(request, 'home/erro.html', {'title':'Erro'})

def busca(request):
    if request.user.is_authenticated():
        clientes = cliente.objects.all().order_by('nome')
        if request.method == 'POST' and request.POST.get('cliente_id') != None:
            cliente_id = request.POST.get('cliente_id')
            ordens_cliente = ordens.objects.filter(cliente_ordem__id=cliente_id).all().order_by('-id')
            return render(request, 'busca_ordem.html', {'title':'Busca Ordens', 'clientes':clientes, 'ordens_cliente':ordens_cliente})
        return render(request, 'busca_ordem.html', {'title':'Busca Ordens', 'clientes':clientes})
    else:
        return render(request, 'home/erro.html', {'title':'Erro'})

def abrir(request):
    if request.user.is_authenticated():
        if request.method == 'POST' and request.POST.get('cliente_id') != None and request.POST.get('servico_id') == None and request.POST.get('produto_id') == None:
            cliente_id = request.POST.get('cliente_id')
            cliente_obj = cliente.objects.filter(id=cliente_id).get()
            ordem_obj = ordens(cliente_ordem=cliente_obj, estado=1, total="0")
            ordem_obj.save()
            produtos1 = ordem_obj.prod_item.all()
            servicos1 = ordem_obj.serv_item.all()
            servicos = servico.objects.all().order_by('nome')
            produtos = produto.objects.all().order_by('nome')
            funcionarios = funcionario.objects.all().order_by('nome')
            return render(request, 'edit_ordem.html', {'title':'Abrir Ordem', 'ordem_obj':ordem_obj, 'produtos1':produtos1, 'servicos1':servicos1, 'produtos':produtos, 'servicos':servicos, 'cliente_id':cliente_id, 'funcionarios':funcionarios})
        elif request.method == 'POST' and request.POST.get('cliente_id') != None and request.POST.get('servico_id') != None and request.POST.get('funcionario_id') != None and request.POST.get('produto_id') == None:
            cliente_id = request.POST.get('cliente_id')
            servico_id = request.POST.get('servico_id')
            qnt_servico = request.POST.get('qnt_servico')
            func_id = request.POST.get('funcionario_id')
            veiculo = request.POST.get('veiculo')
            placa = request.POST.get('placa')
            cliente_obj = cliente.objects.filter(id=cliente_id).get()
            servico_obj = servico.objects.filter(id=servico_id).get()
            func_obj = funcionario.objects.filter(id=func_id).get()
            total_serv = servico_obj.valor * Decimal(qnt_servico)
            novo_servico = servico_item(serv_item = servico_obj, quantidade = qnt_servico, total = total_serv, func = func_obj)
            novo_servico.save()
            ordem_obj = ordens(cliente_ordem=cliente_obj, estado=1,placa=placa, carro=veiculo, total="0")
            ordem_obj.save()
            ordem_obj.serv_item.add(novo_servico)
            ordem_obj.total = novo_servico.total
            ordem_obj.save()
            produtos1 = ordem_obj.prod_item.all()
            servicos1 = ordem_obj.serv_item.all()
            servicos = servico.objects.all().order_by('nome')
            produtos = produto.objects.all().order_by('nome')
            funcionarios = funcionario.objects.all()
            return render(request, 'edit_ordem.html', {'title':'Abrir Ordem', 'ordem_obj':ordem_obj, 'produtos1':produtos1, 'servicos1':servicos1, 'produtos':produtos, 'servicos':servicos, 'cliente_id':cliente_id, 'funcionarios':funcionarios})
        elif request.method == 'POST' and request.POST.get('cliente_id') != None and request.POST.get('servico_id') == None and request.POST.get('produto_id') != None:
            cliente_id = request.POST.get('cliente_id')
            produto_id = request.POST.get('produto_id')
            qnt_produto = request.POST.get('qnt_produto')
            veiculo = request.POST.get('veiculo')
            placa = request.POST.get('placa')
            cliente_obj = cliente.objects.filter(id=cliente_id).get()
            produto_obj = produto.objects.filter(id=produto_id).get()
            total_prod = produto_obj.valor_venda * Decimal(qnt_produto)
            novo_produto = produto_item(prod_item = produto_obj, quantidade = qnt_produto, total = total_prod)
            novo_produto.save()
            ordem_obj = ordens(cliente_ordem=cliente_obj, estado=1,placa=placa, carro=veiculo, total="0")
            ordem_obj.save()
            ordem_obj.prod_item.add(novo_produto)
            ordem_obj.total = novo_produto.total
            ordem_obj.save()
            produtos1 = ordem_obj.prod_item.all()
            servicos1 = ordem_obj.serv_item.all()
            servicos = servico.objects.all().order_by('nome')
            produtos = produto.objects.all().order_by('nome')
            funcionarios = funcionario.objects.all()
            return render(request, 'edit_ordem.html', {'title':'Abrir Ordem', 'ordem_obj':ordem_obj, 'produtos1':produtos1, 'servicos1':servicos1, 'produtos':produtos, 'servicos':servicos, 'cliente_id':cliente_id, 'funcionarios':funcionarios})
        elif request.method == 'POST' and request.POST.get('cliente_id') != None and request.POST.get('servico_id') != None and request.POST.get('produto_id') != None:
            cliente_id = request.POST.get('cliente_id')
            produto_id = request.POST.get('produto_id')
            servico_id = request.POST.get('servico_id')
            qnt_produto = request.POST.get('qnt_produto')
            qnt_servico = request.POST.get('qnt_servico')
            func_id = request.POST.get('funcionario_id')
            veiculo = request.POST.get('veiculo')
            placa = request.POST.get('placa')
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
            ordem_obj = ordens(cliente_ordem=cliente_obj, estado=1,placa=placa, carro=veiculo, total="0")
            ordem_obj.save()
            ordem_obj.prod_item.add(novo_produto)
            ordem_obj.serv_item.add(novo_servico)
            ordem_obj.total = novo_servico.total + novo_produto.total
            ordem_obj.save()
            produtos1 = ordem_obj.prod_item.all()
            servicos1 = ordem_obj.serv_item.all()
            servicos = servico.objects.all().order_by('nome')
            produtos = produto.objects.all().order_by('nome')
            funcionarios = funcionario.objects.all().order_by('nome')
            return render(request, 'edit_ordem.html', {'title':'Abrir Ordem', 'ordem_obj':ordem_obj, 'produtos1':produtos1, 'servicos1':servicos1, 'produtos':produtos, 'servicos':servicos, 'cliente_id':cliente_id, 'funcionarios':funcionarios})
    else:
        return render(request, 'home/erro.html', {'title':'Erro'})

def editar(request):
    if request.user.is_authenticated():
       if request.method == 'GET' and request.GET.get('ordem_id') != None:
            ordem_id = request.GET.get('ordem_id')
            cliente_id = request.GET.get('cliente_id')
            ordem_obj = ordens.objects.filter(id = ordem_id).get()
            produtos1 = ordem_obj.prod_item.all()
            servicos1 = ordem_obj.serv_item.all()
            servicos = servico.objects.all().order_by('nome')
            produtos = produto.objects.all().order_by('nome')
            funcionarios = funcionario.objects.all().order_by('nome')
            return render(request, 'edit_ordem.html', {'title':'Editar Ordens', 'ordem_obj':ordem_obj, 'produtos1':produtos1, 'servicos1':servicos1, 'produtos':produtos, 'servicos':servicos, 'cliente_id':cliente_id, 'funcionarios':funcionarios})
           
    else:
        return render(request, 'home/erro.html', {'title':'Erro'})

def cancellar(request):
    if request.user.is_authenticated():
       if request.method == 'POST' and request.POST.get('prod_item') != None:
            prod_item_id = request.POST.get('prod_item')
            ordem_id = request.POST.get('ordem_id')
            cliente_id = request.POST.get('cliente_id')
            prod_item_obj = produto_item.objects.filter(id = prod_item_id).get()
            prod_preco = Decimal(prod_item_obj.total)
            prod_item_obj.delete()
            ordem_obj = ordens.objects.filter(id=ordem_id).get()
            ordem_obj.total = Decimal(ordem_obj.total) - prod_preco
            ordem_obj.save()
            produtos1 = ordem_obj.prod_item.all()
            servicos1 = ordem_obj.serv_item.all()
            servicos = servico.objects.all().order_by('nome')
            produtos = produto.objects.all().order_by('nome')
            funcionarios = funcionario.objects.all().order_by('nome')
            return render(request, 'edit_ordem.html', {'title':'Editar Ordens', 'ordem_obj':ordem_obj, 'produtos1':produtos1, 'servicos1':servicos1, 'produtos':produtos, 'servicos':servicos, 'cliente_id':cliente_id, 'funcionarios':funcionarios})        
    else:
        return render(request, 'home/erro.html', {'title':'Erro'})

def cancelar(request):
    if request.user.is_authenticated():
       if request.method == 'POST' and request.POST.get('serv_item') != None:
            serv_item_id = request.POST.get('serv_item')
            ordem_id = request.POST.get('ordem_id')
            cliente_id = request.POST.get('cliente_id')
            serv_item_obj = servico_item.objects.filter(id = serv_item_id).get()
            serv_preco = Decimal(serv_item_obj.total)
            serv_item_obj.delete()
            ordem_obj = ordens.objects.filter(id=ordem_id).get()
            ordem_obj.total = Decimal(ordem_obj.total) - serv_preco
            ordem_obj.save()
            produtos1 = ordem_obj.prod_item.all()
            servicos1 = ordem_obj.serv_item.all()
            servicos = servico.objects.all().order_by('nome')
            produtos = produto.objects.all().order_by('nome')
            funcionarios = funcionario.objects.all().order_by('nome')
            return render(request, 'edit_ordem.html', {'title':'Editar Ordens', 'ordem_obj':ordem_obj, 'produtos1':produtos1, 'servicos1':servicos1, 'produtos':produtos, 'servicos':servicos, 'cliente_id':cliente_id, 'funcionarios':funcionarios})        
    else:
        return render(request, 'home/erro.html', {'title':'Erro'})

def fechar(request):
    if request.user.is_authenticated():
        clientes = cliente.objects.all().order_by('nome')
        ordens1 = ordens.objects.filter(estado=1).all().order_by('cliente_ordem')
        if request.method == 'GET' and request.GET.get('ordem_id') != None:
            ordem_id = request.GET.get('ordem_id')
            return render(request, 'metodo_ordem.html', {'title':'Metodo', 'ordem_id':ordem_id})
        elif request.method == 'POST' and request.POST.get('ordem_id') != None and request.POST.get('metodo') != None:
            data = timezone.now()
            ordem_id = request.POST.get('ordem_id')
            metodo = request.POST.get('metodo')
            ordem_obj = ordens.objects.filter(id = ordem_id).get()
            caixa = caixa_geral.objects.latest('id')
            total = caixa.total + ordem_obj.total
            desc = "Ordem numero "+str(ordem_id)+"."
            novo_caixa = caixa_geral(tipo=1, total=total, desc=desc)
            novo_caixa.save()
            ordem_obj.estado = 2
            ordem_obj.data_fechamento = data
            ordem_obj.metodo = metodo
            ordem_obj.save()
            msg = "Ordem finalizada com sucesso"
            return render(request, 'home/index.html', {'title':'Home', 'msg':msg})
        return render(request, 'fechar_ordem.html', {'title':'Fechar Ordens', 'clientes':clientes, 'ordens1':ordens1})
    else:
        return render(request, 'home/erro.html', {'title':'Erro'})

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
            servicos = servico.objects.all().order_by('nome')
            produtos = produto.objects.all().order_by('nome')
            funcionarios = funcionario.objects.all().order_by('nome')
            return render(request, 'edit_ordem.html', {'title':'Abrir Ordem', 'ordem_obj':ordem_obj, 'produtos1':produtos1, 'servicos1':servicos1, 'produtos':produtos, 'servicos':servicos, 'cliente_id':cliente_id, 'funcionarios':funcionarios})
        return render(request, 'edit_ordem.html', {'title':'Editar Ordens', 'clientes':clientes})
    else:
        return render(request, 'home/erro.html', {'title':'Erro'})

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
            servicos = servico.objects.all().order_by('nome')
            produtos = produto.objects.all().order_by('nome')
            funcionarios = funcionario.objects.all().order_by('nome')
            return render(request, 'edit_ordem.html', {'title':'Abrir Ordem', 'ordem_obj':ordem_obj, 'produtos1':produtos1, 'servicos1':servicos1, 'produtos':produtos, 'servicos':servicos, 'cliente_id':cliente_id, 'funcionarios':funcionarios})
        return render(request, 'edit_ordem.html', {'title':'Editar Ordens', 'clientes':clientes})
    else:
        return render(request, 'home/erro.html', {'title':'Erro'})

def pre_imprimir(request):
    if request.user.is_authenticated():
        if request.method == 'GET' and request.GET.get('ordem_id') != None:
            ordem_id = request.GET.get('ordem_id')
            return render(request, 'pre_imprimir.html', {'title':'Imprimir Ordem', 'ordem_id':ordem_id})
        return render(request, 'pre_imprimir.html', {'title':'Imprimir Ordem'})
    else:
        return render(request, 'home/erro.html', {'title':'Erro'})
    
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

def ver(request):
    if request.user.is_authenticated():
       if request.method == 'GET' and request.GET.get('ordem_id') != None :
            ordem_id = request.GET.get('ordem_id')
            cliente_id = request.GET.get('cliente_id')
            ordem_obj = ordens.objects.filter(id = ordem_id).get()
            produtos1 = ordem_obj.prod_item.all()
            servicos1 = ordem_obj.serv_item.all()
            servicos = servico.objects.all().order_by('nome')
            produtos = produto.objects.all().order_by('nome')
            funcionarios = funcionario.objects.all().order_by('nome')
            return render(request, 'ver_ordem.html', {'title':'Ver Ordens', 'ordem_obj':ordem_obj, 'produtos1':produtos1, 'servicos1':servicos1, 'produtos':produtos, 'servicos':servicos, 'cliente_id':cliente_id, 'funcionarios':funcionarios})
           
    else:
        return render(request, 'home/erro.html', {'title':'Erro'})

def total_ordem(request):
    if request.user.is_authenticated():
       if request.method == 'POST' and request.POST.get('cliente_id') != None :
            cliente_id = request.POST.get('cliente_id')
            cliente_ord = cliente.objects.filter(id=cliente_id).get()
            tot_ordem = 0
            tot_ordem_1 = 0
            for e in ordens.objects.filter(cliente_ordem__id = cliente_id, estado='1').all():
                tot_ordem = tot_ordem + e.total

            for j in ordens.objects.filter(cliente_ordem__id = cliente_id, estado='2').all():
                tot_ordem_1 = tot_ordem_1 + j.total

            num_ordens = ordens.objects.filter(cliente_ordem = cliente_id, estado='1').count()

            num_ordens_1 = ordens.objects.filter(cliente_ordem = cliente_id, estado='2').count()
            clientes = cliente.objects.all().order_by('nome')
            return render(request, 'total_ordem.html', {'title':'Total em Ordens','num_ordens':num_ordens,'num_ordens_1':num_ordens_1,'tot_ordem_1':tot_ordem_1, 'cliente_ord':cliente_ord, 'cliente_id':cliente_id, 'tot_ordem':tot_ordem, 'clientes':clientes})
           
    else:
        return render(request, 'home/erro.html', {'title':'Erro'})

def excluir(request):
    if request.user.is_authenticated():
        if request.method == 'GET' and request.GET.get('ordem_id') != None:
            od_id = request.GET.get('ordem_id')
            od_obj = ordens.objects.filter(id=od_id).get()
            od_obj.delete()
            msg = "Ordem Excluida com sucesso"
            return render(request, 'home/index.html', {'title':'Home', 'msg':msg})
    else:
        return render(request, 'home/erro.html', {'title':'Erro'})