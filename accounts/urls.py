from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import (
    HistoriaCreateView, HistoriaUpdateView, HistoriaDeleteView,
    ItemHistoriaCreateView, ItemHistoriaUpdateView, ItemHistoriaDeleteView
)

urlpatterns = [
    path('', views.home, name='home'),
    # path('register/', views.register, name='register'),  # Desabilitado
    path('editar-perfil/', views.editar_perfil, name='editar_perfil'),
    path('login/', auth_views.LoginView.as_view(
        template_name='accounts/login.html',
        authentication_form=views.CustomAuthenticationForm
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        next_page='login'
    ), name='logout'),
    path('confirm-email/<int:user_id>/', views.confirm_email, name='confirm_email'),
    path('configuracoes/', views.configuracoes, name='configuracoes'),
    path('historias/', views.historias, name='historias'),
    path('historias/<int:historia_id>/', views.detalhe_historia, name='detalhe_historia'),
    path('historias/<int:historia_id>/adicionar-item/', views.adicionar_item_historia, name='adicionar_item_historia'),
    path('historias/criar/', HistoriaCreateView.as_view(), name='criar_historia'),
    path('historias/<int:pk>/editar/', HistoriaUpdateView.as_view(), name='editar_historia'),
    path('historias/<int:pk>/deletar/', HistoriaDeleteView.as_view(), name='deletar_historia'),
    path('historias/<int:historia_id>/itens/criar/', ItemHistoriaCreateView.as_view(), name='criar_item_historia'),
    path('itens/<int:pk>/editar/', ItemHistoriaUpdateView.as_view(), name='editar_item_historia'),
    path('itens/<int:pk>/deletar/', ItemHistoriaDeleteView.as_view(), name='deletar_item_historia'),
    
    # URLs Administrativas
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('manage-users/', views.manage_users, name='manage_users'),
    path('admin-editar-usuario/<int:user_id>/', views.admin_editar_usuario, name='admin_editar_usuario'),
] 