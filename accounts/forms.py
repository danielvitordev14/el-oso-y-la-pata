from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Historia, ItemHistoria

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')
    filha_nome = forms.CharField(required=True, label='Nome da Filha')
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'filha_nome', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.filha_nome = self.cleaned_data['filha_nome']
        if commit:
            user.save()
        return user

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label='Email ou Nome de Usuário',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite seu email ou nome de usuário'
        })
    )

class HistoriaForm(forms.ModelForm):
    musica_youtube = forms.URLField(
        label='Link da música do YouTube',
        required=False,
        widget=forms.URLInput(attrs={
            'class': 'form-control',
            'placeholder': 'https://www.youtube.com/watch?v=...'
        })
    )
    class Meta:
        model = Historia
        fields = ['titulo', 'musica_youtube']
        labels = {'titulo': 'Título da História'}
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título da história'})
        }

class ItemHistoriaForm(forms.ModelForm):
    texto = forms.CharField(
        label='Texto (opcional)',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Digite o texto que aparecerá com a imagem (opcional)...'
        }),
        help_text='Deixe em branco se quiser apenas a imagem.'
    )
    
    class Meta:
        model = ItemHistoria
        fields = ['foto', 'texto', 'ordem']
        labels = {
            'foto': 'Foto',
            'texto': 'Texto (opcional)',
            'ordem': 'Ordem do Item'
        }
        widgets = {
            'foto': forms.FileInput(attrs={'class': 'form-control'}),
            'ordem': forms.NumberInput(attrs={'class': 'form-control'})
        }

class EditarPerfilForm(forms.ModelForm):
    texto_inicio = forms.CharField(
        label='Texto de Início',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Digite aqui o texto que aparecerá na sua tela inicial...'
        }),
        help_text='Este texto será exibido na sua tela inicial de boas-vindas.'
    )
    
    filha_nome = forms.CharField(
        label='Nome da Filha',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nome da sua filha'
        })
    )
    
    class Meta:
        model = CustomUser
        fields = ['filha_nome', 'texto_inicio']

class AdminEditarUsuarioForm(forms.ModelForm):
    nova_senha = forms.CharField(
        label='Nova Senha',
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Deixe em branco para manter a senha atual'
        }),
        help_text='Deixe em branco para manter a senha atual.'
    )
    
    confirmar_senha = forms.CharField(
        label='Confirmar Nova Senha',
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirme a nova senha'
        })
    )
    
    username = forms.CharField(
        label='Nome de Usuário',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    
    filha_nome = forms.CharField(
        label='Nome da Filha',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    texto_inicio = forms.CharField(
        label='Texto de Início',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Texto personalizado para a tela inicial...'
        })
    )
    
    is_admin = forms.BooleanField(
        label='É Administrador',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    email_confirmed = forms.BooleanField(
        label='Email Confirmado',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    is_active = forms.BooleanField(
        label='Usuário Ativo',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'filha_nome', 'texto_inicio', 'is_admin', 'email_confirmed', 'is_active']
    
    def clean(self):
        cleaned_data = super().clean()
        nova_senha = cleaned_data.get('nova_senha')
        confirmar_senha = cleaned_data.get('confirmar_senha')
        
        if nova_senha and nova_senha != confirmar_senha:
            raise forms.ValidationError('As senhas não coincidem.')
        
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        nova_senha = self.cleaned_data.get('nova_senha')
        
        if nova_senha:
            user.set_password(nova_senha)
        
        # Atualizar is_staff baseado em is_admin
        user.is_staff = user.is_admin
        
        if commit:
            user.save()
        return user 