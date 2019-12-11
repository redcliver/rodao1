from django.shortcuts import render
import datetime

# Create your views here.
def loginPage(request):
    return render (request, 'loginPage/login.html', {'title':'Login'})