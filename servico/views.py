from django.shortcuts import render
from django.contrib.auth import authenticate

# Create your views here.
def servico1(request):
    if request.user.is_authenticated():
        return render(request, 'servico.html', {'title':'Serviço'})
    else:
        return render(request, 'erro.html', {'title':'Erro'})

def busca1(request):
    if request.user.is_authenticated():
        return render(request, 'busca_servico.html', {'title':'Busca Serviço'})
    else:
        return render(request, 'erro.html', {'title':'Erro'})

def editar1(request):
    if request.user.is_authenticated():
        return render(request, 'edit_servico.html', {'title':'Editar Serviço'})
    else:
        return render(request, 'erro.html', {'title':'Erro'})