from django.shortcuts import render
from django.contrib.auth import authenticate
from django.utils import timezone
from datetime import datetime
from ordem.models import ordens
from contas.models import conta

# Create your views here.
def home(request):
    if request.user.is_authenticated():
        try:
            ordem_aberta = ordens.objects.filter(estado=1).count()
        except:
            ordem_aberta = 0
        contas = 0
        hoje = timezone.now()
        for e in conta.objects.filter(estado=1).all():
            if e.data <= timezone.now():
                contas = contas + 1
            else:
                contas = contas
        n_ordem = ordem_aberta
        n_contas =  contas
        return render(request, 'home/index.html', {'title':'Home', 'n_ordem':n_ordem, 'n_contas':n_contas, 'hoje':hoje})
    else:
        return render(request, 'home/erro.html', {'title':'Erro'})