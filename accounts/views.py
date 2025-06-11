from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm, HistoriaForm, ItemHistoriaForm, EditarPerfilForm, AdminEditarUsuarioForm
from .models import CustomUser, Historia, ItemHistoria
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .decorators import admin_required, admin_required_message

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Enviar email de confirmação
            subject = 'Confirme seu email'
            html_message = render_to_string('accounts/email_confirmation.html', {
                'user': user,
                'confirmation_link': f"http://{request.get_host()}/confirm-email/{user.id}/"
            })
            plain_message = strip_tags(html_message)
            send_mail(
                subject,
                plain_message,
                settings.EMAIL_HOST_USER,
                [user.email],
                html_message=html_message,
                fail_silently=False,
            )
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def confirm_email(request, user_id):
    try:
        user = CustomUser.objects.get(id=user_id)
        user.email_confirmed = True
        user.save()
        return redirect('login')
    except CustomUser.DoesNotExist:
        return redirect('login')

@login_required
def home(request):
    return render(request, 'accounts/home.html')

@login_required
def editar_perfil(request):
    if request.method == 'POST':
        form = EditarPerfilForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('editar_perfil')
    else:
        form = EditarPerfilForm(instance=request.user)
    
    return render(request, 'accounts/editar_perfil.html', {'form': form})

@admin_required_message
def configuracoes(request):
    # Apenas administradores podem acessar configurações
    historias = Historia.objects.filter(usuario=request.user)  # Admins veem suas próprias histórias na configuração
    if request.method == 'POST':
        historia_form = HistoriaForm(request.POST)
        if historia_form.is_valid():
            historia = historia_form.save(commit=False)
            historia.usuario = request.user
            historia.save()
            messages.success(request, f'História "{historia.titulo}" criada com sucesso!')
            return redirect('configuracoes')
    else:
        historia_form = HistoriaForm()
    return render(request, 'accounts/configuracoes.html', {
        'historias': historias,
        'historia_form': historia_form
    })

@login_required
def adicionar_item_historia(request, historia_id):
    historia = Historia.objects.get(id=historia_id, usuario=request.user)
    if request.method == 'POST':
        form = ItemHistoriaForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.historia = historia
            item.save()
            return redirect('detalhe_historia', historia_id=historia.id)
    else:
        form = ItemHistoriaForm()
    return render(request, 'accounts/adicionar_item_historia.html', {'form': form, 'historia': historia})

@login_required
def historias(request):
    # Mostra todas as histórias de todos os usuários
    historias = Historia.objects.all().order_by('-criado_em').select_related('usuario')
    return render(request, 'accounts/historias.html', {'historias': historias})

@login_required
def detalhe_historia(request, historia_id):
    # Todos podem ver qualquer história, mas só o dono ou admin pode editar
    historia = get_object_or_404(Historia, id=historia_id)
    itens = historia.itens.order_by('ordem')
    
    # Verifica se o usuário pode editar (é o dono ou é admin)
    can_edit = (historia.usuario == request.user) or getattr(request.user, 'is_admin', False)
    
    return render(request, 'accounts/detalhe_historia.html', {
        'historia': historia, 
        'itens': itens,
        'can_edit': can_edit
    })

class HistoriaCreateView(LoginRequiredMixin, CreateView):
    model = Historia
    form_class = HistoriaForm
    template_name = 'accounts/historia_form.html'
    success_url = reverse_lazy('configuracoes')
    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)

class HistoriaUpdateView(LoginRequiredMixin, UpdateView):
    model = Historia
    form_class = HistoriaForm
    template_name = 'accounts/historia_form.html'
    success_url = reverse_lazy('configuracoes')
    def get_queryset(self):
        return Historia.objects.filter(usuario=self.request.user)

class HistoriaDeleteView(LoginRequiredMixin, DeleteView):
    model = Historia
    template_name = 'accounts/historia_confirm_delete.html'
    success_url = reverse_lazy('configuracoes')
    def get_queryset(self):
        return Historia.objects.filter(usuario=self.request.user)

class ItemHistoriaCreateView(LoginRequiredMixin, CreateView):
    model = ItemHistoria
    form_class = ItemHistoriaForm
    template_name = 'accounts/item_historia_form.html'
    success_url = reverse_lazy('configuracoes')
    def form_valid(self, form):
        historia = Historia.objects.get(id=self.kwargs['historia_id'], usuario=self.request.user)
        form.instance.historia = historia
        return super().form_valid(form)

class ItemHistoriaUpdateView(LoginRequiredMixin, UpdateView):
    model = ItemHistoria
    form_class = ItemHistoriaForm
    template_name = 'accounts/item_historia_form.html'
    success_url = reverse_lazy('configuracoes')
    def get_queryset(self):
        return ItemHistoria.objects.filter(historia__usuario=self.request.user)

class ItemHistoriaDeleteView(LoginRequiredMixin, DeleteView):
    model = ItemHistoria
    template_name = 'accounts/item_historia_confirm_delete.html'
    success_url = reverse_lazy('configuracoes')
    def get_queryset(self):
        return ItemHistoria.objects.filter(historia__usuario=self.request.user)

# === VIEWS ADMINISTRATIVAS ===

@admin_required_message
def admin_dashboard(request):
    """Dashboard administrativo - somente para administradores"""
    total_users = CustomUser.objects.count()
    total_admins = CustomUser.objects.filter(is_admin=True).count()
    total_historias = Historia.objects.count()
    total_itens = ItemHistoria.objects.count()
    recent_users = CustomUser.objects.order_by('-date_joined')[:5]
    
    context = {
        'total_users': total_users,
        'total_admins': total_admins,
        'total_historias': total_historias,
        'total_itens': total_itens,
        'recent_users': recent_users,
    }
    return render(request, 'accounts/admin_dashboard.html', context)

@admin_required_message
def manage_users(request):
    """Gerenciar usuários - somente para administradores"""
    users = CustomUser.objects.all().order_by('-date_joined')
    
    # Se for uma requisição POST, pode ser para promover/rebaixar usuário
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        action = request.POST.get('action')
        
        if user_id and action:
            user = get_object_or_404(CustomUser, id=user_id)
            
            if action == 'promote' and not user.is_admin:
                user.is_admin = True
                user.is_staff = True
                user.save()
                messages.success(request, f'Usuário {user.username} foi promovido a administrador com sucesso!')
                return redirect('manage_users')
                
            elif action == 'demote' and user.is_admin and user != request.user:
                user.is_admin = False
                user.is_staff = False
                user.save()
                messages.success(request, f'Usuário {user.username} foi rebaixado para usuário comum com sucesso!')
                return redirect('manage_users')
    
    context = {
        'users': users,
    }
    return render(request, 'accounts/manage_users.html', context)

@admin_required_message
def admin_editar_usuario(request, user_id):
    """Editar usuário - somente para administradores"""
    usuario_editado = get_object_or_404(CustomUser, id=user_id)
    
    if request.method == 'POST':
        form = AdminEditarUsuarioForm(request.POST, instance=usuario_editado)
        if form.is_valid():
            form.save()
            messages.success(request, f'Usuário {usuario_editado.username} atualizado com sucesso!')
            return redirect('manage_users')
    else:
        form = AdminEditarUsuarioForm(instance=usuario_editado)
    
    context = {
        'form': form,
        'usuario_editado': usuario_editado,
    }
    return render(request, 'accounts/admin_editar_usuario.html', context)
