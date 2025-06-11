from django import template
from django.contrib.auth import get_user_model

register = template.Library()
User = get_user_model()

@register.filter
def is_admin(user):
    """
    Template filter para verificar se o usuário é administrador.
    Uso: {% if user|is_admin %}
    """
    if not user or not user.is_authenticated:
        return False
    return getattr(user, 'is_admin', False)

@register.filter
def user_type(user):
    """
    Template filter para obter o tipo de usuário.
    Uso: {{ user|user_type }}
    """
    if not user or not user.is_authenticated:
        return "Usuário não autenticado"
    return user.get_user_type() if hasattr(user, 'get_user_type') else "Usuário Comum"

@register.simple_tag
def can_access_admin_area(user):
    """
    Template tag para verificar se o usuário pode acessar área administrativa.
    Uso: {% can_access_admin_area user as can_access %}
    """
    if not user or not user.is_authenticated:
        return False
    return getattr(user, 'is_admin', False)

@register.inclusion_tag('accounts/admin_badge.html')
def show_admin_badge(user):
    """
    Template tag de inclusão para mostrar badge de administrador.
    Uso: {% show_admin_badge user %}
    """
    return {
        'user': user,
        'is_admin': getattr(user, 'is_admin', False) if user and user.is_authenticated else False
    } 