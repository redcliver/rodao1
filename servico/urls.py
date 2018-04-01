from django.conf.urls import url
from . import views
from django.contrib.auth.views import login


urlpatterns = [
    url(r'^$', views.servico1),
    url(r'^busca', views.busca1),
    url(r'^editar', views.editar1),
    ]