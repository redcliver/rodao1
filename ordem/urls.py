from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.ordem),
    url(r'^busca', views.busca),
    url(r'^abrir', views.abrir),
    url(r'^editar', views.editar),
    url(r'^imprimir', views.imprimir),
    url(r'^ver', views.ver),
    url(r'^add_serv', views.add_serv),
    url(r'^add_prod', views.add_prod),
    url(r'^fechar', views.fechar),
    ]
