"""
Views para autenticação de usuários
(Login, Signup, Logout)
"""
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages


def login_view(request):
    """View para login de usuários"""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(
                request,
                f'Bem-vindo de volta, {user.username}!'
            )
            next_url = request.GET.get('next', 'dashboard')
            return redirect(next_url)
        else:
            messages.error(request, 'Usuário ou senha incorretos.')

    return render(request, 'login.html')


def signup_view(request):
    """View para cadastro de novos usuários"""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        # Validações
        if password != password_confirm:
            messages.error(request, 'As senhas não coincidem.')
            return render(request, 'signup.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Este nome de usuário já está em uso.')
            return render(request, 'signup.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Este e-mail já está cadastrado.')
            return render(request, 'signup.html')

        # Criar usuário
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # Fazer login automático
        login(request, user)
        messages.success(request, 'Conta criada com sucesso! Bem-vindo!')
        return redirect('dashboard')

    return render(request, 'signup.html')


def logout_view(request):
    """View para logout de usuários"""
    logout(request)
    messages.success(request, 'Você saiu com sucesso.')
    return redirect('login')
