from django.shortcuts import render
from django.contrib.auth import authenticate
from ordem.models import ordens
from contas.models import conta

# Create your views here.
def home(request):
    if request.user.is_authenticated():
        try:
            ordem_aberta = ordens.objects.filter(estado=1).count()
        except:
            ordem_aberta = 0
        try:
            contas = conta.objects.filter(estado=1).count()
        except:
            contas = 0
        msg = "Ola, temos "+str(ordem_aberta)+" ordens em aberto;"
        msg1 = "  - "+str(contas)+" Contas a pagar;"
        return render(request, 'home/index.html', {'title':'Home', 'msg':msg, 'msg1':msg1})
    else:
        return render(request, 'home/erro.html', {'title':'Erro'})