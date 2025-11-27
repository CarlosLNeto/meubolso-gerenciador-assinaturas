"""
URL configuration for meubolso project.

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
from assinaturas import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Autenticação
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    
    # Assinaturas
    path('assinaturas/', views.listar_assinaturas, name='assinaturas'),
    path('assinaturas/nova/', views.criar_assinatura, name='criar_assinatura'),
    path('assinaturas/<int:id>/editar/', views.editar_assinatura, name='editar_assinatura'),
    path('assinaturas/<int:id>/deletar/', views.deletar_assinatura, name='deletar_assinatura'),
    
    # Categorias
    path('categorias/', views.listar_categorias, name='categorias'),
    path('categorias/nova/', views.criar_categoria, name='criar_categoria'),
    path('categorias/<int:id>/editar/', views.editar_categoria, name='editar_categoria'),
    path('categorias/<int:id>/deletar/', views.deletar_categoria, name='deletar_categoria'),
]
