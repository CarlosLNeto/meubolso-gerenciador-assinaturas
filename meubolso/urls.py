"""
URL configuration for meubolso project.

URLs estruturadas seguindo boas práticas de SEO:
- URLs descritivas e semânticas
- Hierarquia clara
- Verbos HTTP apropriados (REST-like)
"""
from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from assinaturas import views

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # SEO: Robots.txt
    path('robots.txt', RedirectView.as_view(url=settings.STATIC_URL + 'robots.txt', permanent=True)),
    
    # Dashboard (Página inicial)
    path('', views.dashboard, name='dashboard'),
    path('dashboard/', views.dashboard, name='dashboard_alt'),  # URL alternativa
    
    # Autenticação - URLs semânticas
    path('entrar/', views.login_view, name='login'),
    path('cadastro/', views.signup_view, name='signup'),
    path('sair/', views.logout_view, name='logout'),
    
    # Assinaturas - Estrutura RESTful
    path('assinaturas/', views.listar_assinaturas, name='assinaturas'),
    path('assinaturas/nova/', views.criar_assinatura, name='criar_assinatura'),
    path('assinaturas/<int:id>/editar/', views.editar_assinatura, name='editar_assinatura'),
    path('assinaturas/<int:id>/deletar/', views.deletar_assinatura, name='deletar_assinatura'),
    
    # Categorias - Estrutura RESTful
    path('categorias/', views.listar_categorias, name='categorias'),
    path('categorias/nova/', views.criar_categoria, name='criar_categoria'),
    path('categorias/<int:id>/editar/', views.editar_categoria, name='editar_categoria'),
    path('categorias/<int:id>/deletar/', views.deletar_categoria, name='deletar_categoria'),
    
    # Configurações
    path('configuracoes/', views.configuracoes, name='configuracoes'),
]

# Servir arquivos estáticos em desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
