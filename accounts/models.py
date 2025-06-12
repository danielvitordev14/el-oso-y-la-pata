from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from cloudinary_storage.storage import MediaCloudinaryStorage

# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    filha_nome = models.CharField(_('nome da filha'), max_length=100)
    email_confirmed = models.BooleanField(default=False)
    is_admin = models.BooleanField(_('é administrador'), default=False, help_text=_('Determina se o usuário tem privilégios de administrador.'))
    texto_inicio = models.TextField(_('texto de início'), blank=True, null=True, help_text=_('Texto personalizado para exibir na tela inicial.'))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'filha_nome']

    def __str__(self):
        return self.email
    
    def is_administrator(self):
        """Retorna True se o usuário é administrador"""
        return self.is_admin
    
    def get_user_type(self):
        """Retorna o tipo de usuário como string"""
        return "Administrador" if self.is_admin else "Usuário Comum"

class Historia(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='historias')
    titulo = models.CharField(max_length=200)
    criado_em = models.DateTimeField(auto_now_add=True)
    musica_youtube = models.URLField('Link da música do YouTube', blank=True, null=True)

    def __str__(self):
        return self.titulo

class ItemHistoria(models.Model):
    historia = models.ForeignKey(Historia, on_delete=models.CASCADE, related_name='itens')
    foto = models.ImageField(upload_to='historias_fotos/', storage=MediaCloudinaryStorage())
    texto = models.TextField(blank=True, null=True)
    ordem = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Item {self.ordem} da história '{self.historia.titulo}'"
