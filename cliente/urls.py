from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.cliente_view),
    url(r'^juridico', views.juridico),
    url(r'^busca', views.busca),
    url(r'^editar', views.editar),
    ]