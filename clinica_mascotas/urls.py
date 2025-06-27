"""
URL configuration for clinica_mascotas project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Clinica.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('inicio/', inicio, name='inicio'),
    path('agendar/',AgendarCitas, name='agendar_citas'),
    path('cargar-animales/', cargar_animales, name='ajax_cargar_animales'),
    path('propietarios/agregar/', agregar_propietario, name='agregar_propietario'),
    path('propietarios/', lista_propietarios, name='propietarios_lista'),
        path('propietarios/<int:propietario_id>/editar/',editar_propietario, name='editar_propietario'),
    path('propietarios/<int:propietario_id>/eliminar/', eliminar_propietario, name='eliminar_propietario'),
    path('historial/<int:animal_id>/', historial_citas, name='historial_citas'),
]
