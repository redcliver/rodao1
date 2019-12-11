from django.shortcuts import render
import datetime

# Create your views here.
def loginPage(request):
    return render (request, 'mainPage/login.html', {'title':'Login'})