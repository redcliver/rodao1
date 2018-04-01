from django.shortcuts import render
from django.contrib.auth import authenticate
from produto.models import produto

# Create your views here.
def produto1(request):
    if request.user.is_authenticated():
        if request.method == 'POST' and request.POST.get('name'):
            name = request.POST.get('name')
            valor_vend = request.POST.get('valor_vend')
            qnt = request.POST.get('qnt')
            novo_produto = produto(nome=name, valor_venda=valor_vend, quantidade=qnt)
            novo_produto.save()
            return render(request, 'produto.html', {'title':'Produto'})
        return render(request, 'produto.html', {'title':'Produto'})
    else:
        return render(request, 'erro.html', {'title':'Erro'})

def busca1(request):
    if request.user.is_authenticated():
        if request.method == 'GET' and request.GET.get('name') != None:
            name = request.GET.get('name')
            produtos = produto.objects.filter(nome__icontains=name)
            return render(request, 'busca_produto.html', {'title':'Busca Produto', 'produtos':produtos})
        elif request.method == 'POST':
            produto_id = request.POST.get('id')
            produto_obj = produto.objects.filter(id=produto_id).get()

            return render(request, 'edit_produto.html', {'title':'Editar Produto', 'produto_obj':produto_obj})
        return render(request, 'busca_produto.html', {'title':'Busca Produto'})
    else:
        return render(request, 'erro.html', {'title':'Erro'})

def editar1(request):
    if request.user.is_authenticated():
        if request.method == 'POST' and request.POST.get('id') != None:
            produto_id = request.POST.get('id')
            produto_obj = produto.objects.filter(id=produto_id).get()
            produto_nome = request.POST.get('name')
            produto_valor = request.POST.get('valor_vend')
            produto_qnt = request.POST.get('qnt')
            produto_obj.nome = produto_nome
            produto_obj.valor_venda = produto_valor
            produto_obj.quantidade = produto_qnt
            produto_obj.save()
            return render(request, 'home.html', {'title':'Home'})
    else:
        return render(request, 'erro.html', {'title':'Erro'})