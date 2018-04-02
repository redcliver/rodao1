from django.shortcuts import render
from django.contrib.auth import authenticate
from servico.models import servico

# Create your views here.
def servico1(request):
    if request.user.is_authenticated():
        if request.method == 'POST' and request.POST.get('name') != None:
            name = request.POST.get('name')
            val = request.POST.get('valor')
            novo_servico = servico(nome=name, valor=val)
            novo_servico.save()
            return render(request, 'servico.html', {'title':'Servico'})
        return render(request, 'servico.html', {'title':'Servico'})
    else:
        return render(request, 'erro.html', {'title':'Erro'})

def busca1(request):
    if request.user.is_authenticated():
        if request.method == 'GET' and request.GET.get('name') != None:
            name = request.GET.get('name')
            servicos = servico.objects.filter(nome__icontains=name)
            return render(request, 'busca_servico.html', {'title':'Busca Servicos', 'servicos':servicos})
        elif request.method == 'POST':
            servico_id = request.POST.get('id')
            servico_obj = servico.objects.filter(id=servico_id).get()

            return render(request, 'edit_servico.html', {'title':'Editar Servico', 'servico_obj':servico_obj})
        return render(request, 'busca_servico.html', {'title':'Busca Servico'})
    else:
        return render(request, 'erro.html', {'title':'Erro'})

def editar1(request):
    if request.user.is_authenticated():
        if request.method == 'POST' and request.POST.get('id') != None:
            servico_id = request.POST.get('id')
            servico_obj = servico.objects.filter(id=servico_id).get()
            servico_nome = request.POST.get('name')
            servico_val = request.POST.get('valor')
            servico_obj.nome = servico_nome
            servico_obj.valor = servico_val
            servico_obj.save()
            return render(request, 'home.html', {'title':'Home'})
    else:
        return render(request, 'erro.html', {'title':'Erro'})