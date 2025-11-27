"""
Views para configurações do usuário
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm


@login_required(login_url='login')
def configuracoes(request):
    """
    View para página de configurações do usuário
    """
    if request.method == 'POST':
        action = request.POST.get('action')
        
        # Atualizar informações do perfil
        if action == 'update_profile':
            first_name = request.POST.get('first_name', '').strip()
            last_name = request.POST.get('last_name', '').strip()
            email = request.POST.get('email', '').strip()
            
            # Validações básicas
            if not email:
                messages.error(request, 'O email é obrigatório.')
            else:
                request.user.first_name = first_name
                request.user.last_name = last_name
                request.user.email = email
                request.user.save()
                messages.success(request, 'Perfil atualizado com sucesso!')
            
            return redirect('configuracoes')
        
        # Alterar senha
        elif action == 'change_password':
            current_password = request.POST.get('current_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            
            # Validar senha atual
            if not request.user.check_password(current_password):
                messages.error(request, 'Senha atual incorreta.')
            elif new_password != confirm_password:
                messages.error(request, 'As senhas não coincidem.')
            elif len(new_password) < 6:
                messages.error(request, 'A senha deve ter no mínimo 6 caracteres.')
            else:
                request.user.set_password(new_password)
                request.user.save()
                update_session_auth_hash(request, request.user)
                messages.success(request, 'Senha alterada com sucesso!')
            
            return redirect('configuracoes')
    
    # Estatísticas do usuário
    total_assinaturas = request.user.assinaturas.count()
    assinaturas_ativas = request.user.assinaturas.filter(status='ATIVA').count()
    total_categorias = request.user.categorias.count()
    
    # Calcular gasto total
    gasto_mensal = sum(
        a.valor_mensal() 
        for a in request.user.assinaturas.filter(status='ATIVA')
    )
    
    context = {
        'total_assinaturas': total_assinaturas,
        'assinaturas_ativas': assinaturas_ativas,
        'total_categorias': total_categorias,
        'gasto_mensal': gasto_mensal,
    }
    
    return render(request, 'configuracoes.html', context)
