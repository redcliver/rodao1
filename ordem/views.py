from django.shortcuts import render

# Create your views here.
def ordem(request):
    if request.user.is_authenticated():
        return render(request, 'ordem.html', {'title':'Ordem'})
    else:
        return render(request, 'erro.html', {'title':'Erro'})

def busca(request):
    if request.user.is_authenticated():
        return render(request, 'busca_ordem.html', {'title':'Busca Ordens'})
    else:
        return render(request, 'erro.html', {'title':'Erro'})

def abrir(request):
    if request.user.is_authenticated():
        return render(request, 'abrir_ordem.html', {'title':'Abrir Ordem'})
    else:
        return render(request, 'erro.html', {'title':'Erro'})

def editar(request):
    if request.user.is_authenticated():
        return render(request, 'edit_ordem.html', {'title':'Editar Ordem'})
    else:
        return render(request, 'erro.html', {'title':'Erro'})

def fechar(request):
    if request.user.is_authenticated():
        return render(request, 'fechar_ordem.html', {'title':'Fechar Ordens'})
    else:
        return render(request, 'erro.html', {'title':'Erro'})