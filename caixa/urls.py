from django.conf.urls import url
from . import views
from django.contrib.auth.views import login


urlpatterns = [
    url(r'^$', views.caixa1),
    url(r'^retirada', views.retirada),
    url(r'^fechar', views.fechar),
    url(r'^inf_geral', views.inf_geral),
    ]