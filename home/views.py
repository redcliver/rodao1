from django.shortcuts import render
from django.contrib.auth import authenticate

# Create your views here.
def home(request):
    if request.user.is_authenticated():
        msg = "Ola, temos ordens em aberto."
        return render(request, 'home/index.html', {'title':'Home', 'msg':msg})
    else:
        return render(request, 'home/erro.html', {'title':'Erro'})