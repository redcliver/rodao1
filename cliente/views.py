from django.shortcuts import render
from django.contrib.auth import authenticate
# Create your views here.
def cliente_view(request):
    if request.user.is_authenticated():

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
        return render(request, 'busca_cliente.html', {'title':'Busca Clientes'})
    else:
        return render(request, 'erro.html', {'title':'Erro'})

def editar(request):
    if request.user.is_authenticated():

        return render(request, 'edit_cliente_fisico.html', {'title':'Home'})
    else:
        return render(request, 'erro.html', {'title':'Erro'})