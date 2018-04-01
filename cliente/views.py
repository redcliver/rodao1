from django.shortcuts import render
from django.contrib.auth import authenticate
from cliente.models import cliente
from django.contrib import messages

# Create your views here.
def cliente_view(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            name = request.POST.get('name')
            tel = request.POST.get('tel')
            cel = request.POST.get('cel')
            mail = request.POST.get('mail')
            novo_cliente = cliente(nome=name, telefone=tel, celular=cel, email=mail)
            novo_cliente.save()
            messages.success(request, 'Cliente salvo com sucesso')
            return render(request, 'cliente_fisico.html', {'title':'Clientes Fisicos'})
        return render(request, 'cliente_fisico.html', {'title':'Clientes Fisicos'})
    else:
        return render(request, 'erro.html', {'title':'Erro'})

def juridico(request):
    if request.user.is_authenticated():
        return render(request, 'cliente_juridico.html', {'title':'Clientes Juridicos'})
    else:
        return render(request, 'erro.html', {'title':'Erro'})

def busca(request):
    if request.user.is_authenticated():
        if request.method == 'GET' and request.GET.get('name') != None:
            name = request.GET.get('name')
            clientes = cliente.objects.filter(nome__icontains=name)
            return render(request, 'busca_cliente.html', {'title':'Busca Clientes', 'clientes':clientes})
        elif request.method == 'POST':
            cliente_id = request.POST.get('id')
            cliente_obj = cliente.objects.filter(id=cliente_id).get()
            return render(request, 'edit_cliente_fisico.html', {'title':'Editar Clientes Fisico', 'cliente_obj':cliente_obj})
        return render(request, 'busca_cliente.html', {'title':'Busca Clientes'})
    else:
        return render(request, 'erro.html', {'title':'Erro'})

def editar(request):
    if request.user.is_authenticated():
        if request.method == 'POST' and request.POST.get('id') != None:
            cliente_id = request.POST.get('id')
            cliente_obj = cliente.objects.filter(id=cliente_id).get()
            cliente_nome = request.POST.get('name')
            cliente_tel = request.POST.get('tel')
            cliente_cel = request.POST.get('cel')
            cliente_email = request.POST.get('mail')
            cliente_obj.nome = cliente_nome
            cliente_obj.telefone = cliente_tel
            cliente_obj.celular = cliente_cel
            cliente_obj.email = cliente_email
            cliente_obj.save()
            return render(request, 'home.html', {'title':'Home'})
    else:
        return render(request, 'erro.html', {'title':'Erro'})


    