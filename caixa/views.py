from django.shortcuts import render
from caixa.models import caixa_geral
# Create your views here.
def caixa1(request):
    if request.user.is_authenticated():
        try:
            caixa = caixa_geral.objects.latest('id')
            total = caixa.total
        except:
            caixa = caixa_geral(tipo=1, total=0, desc="abertura")
            caixa.save()
            total = caixa.total
        entrada = caixa_geral.objects.filter(tipo=1).count()
        saida = caixa_geral.objects.filter(tipo=2).count()
        return render(request, 'caixa.html', {'title':'Caixa', 'total':total, 'entrada':entrada, 'saida':saida})
    else:
        return render(request, 'home/erro.html', {'title':'Erro'})