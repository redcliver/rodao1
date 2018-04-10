from django.shortcuts import render
from funcionario.models import funcionario

# Create your views here.
def func(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            name = request.POST.get('name')
            tel = request.POST.get('tel')
            cel = request.POST.get('cel')
            mail = request.POST.get('mail')
            novo_func = funcionario(nome=name, telefone=tel, celular=cel, email=mail)
            novo_func.save()
            msg = 'Funcionario Salvo com Sucesso'
            return render(request, 'home/index.html', {'title':'Home', 'msg':msg})
        return render(request, 'funcionario.html', {'title':'Funcionario'})
    else:
        return render(request, 'home/erro.html', {'title':'Erro'})

def busca(request):
    if request.user.is_authenticated():
        if request.method == 'GET' and request.GET.get('name') != None:
            name = request.GET.get('name')
            funcs = funcionario.objects.filter(nome__icontains=name)
            return render(request, 'busca_func.html', {'title':'Busca Funcionario', 'funcs':funcs})
        elif request.method == 'POST':
            func_id = request.POST.get('id')
            func_obj = funcionario.objects.filter(id=func_id).get()
            return render(request, 'edit_func.html', {'title':'Editar Funcionario', 'func_obj':func_obj})
        return render(request, 'busca_func.html', {'title':'Busca Funcionario'})
    else:
        return render(request, 'home/erro.html', {'title':'Erro'})

def editar(request):
    if request.user.is_authenticated():
        if request.method == 'POST' and request.POST.get('id') != None:
            func_id = request.POST.get('id')
            func_obj = funcionario.objects.filter(id=func_id).get()
            func_nome = request.POST.get('name')
            func_tel = request.POST.get('tel')
            func_cel = request.POST.get('cel')
            func_email = request.POST.get('mail')
            func_obj.nome = func_nome
            func_obj.telefone = func_tel
            func_obj.celular = func_cel
            func_obj.email = func_email
            func_obj.save()
            msg = 'Funcionario editado com sucesso'
            return render(request, 'home/index.html', {'title':'Home', 'msg':msg})
    else:
        return render(request, 'home/erro.html', {'title':'Erro'})