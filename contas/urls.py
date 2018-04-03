from django.conf.urls import url
from . import views
from django.contrib.auth.views import login


urlpatterns = [
    url(r'^$', views.conta1),
    url(r'^busca', views.busca1),
    url(r'^editar', views.editar1),
    url(r'^pagar', views.pagar),
    ]
