from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

def admin_required(function=None, redirect_field_name=None, login_url=None):
    """
    Decorator para views que requerem que o usuário seja administrador.
    Se o usuário não for administrador, retorna erro 403.
    """
    def check_admin(user):
        return user.is_authenticated and user.is_admin
    
    actual_decorator = user_passes_test(
        check_admin,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    
    if function:
        return actual_decorator(function)
    return actual_decorator

def admin_required_message(view_func):
    """
    Decorator alternativo que redireciona para home com mensagem
    se o usuário não for administrador.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        
        if not request.user.is_admin:
            messages.error(request, 'Você precisa ser administrador para acessar esta página.')
            return redirect('home')
        
        return view_func(request, *args, **kwargs)
    return wrapper

def is_admin_or_owner(user, obj):
    """
    Função helper que verifica se o usuário é admin ou dono do objeto.
    Útil para views que permitem acesso ao admin ou ao proprietário.
    """
    if not user.is_authenticated:
        return False
    
    return user.is_admin or (hasattr(obj, 'usuario') and obj.usuario == user) 