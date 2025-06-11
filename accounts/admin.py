from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from django import forms
from .models import CustomUser, Historia, ItemHistoria

class CustomUserAdminForm(forms.ModelForm):
    texto_inicio = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 60}),
        required=False,
        help_text='Texto personalizado que aparecerá na tela inicial do usuário.'
    )
    
    class Meta:
        model = CustomUser
        fields = '__all__'

class CustomUserAdmin(UserAdmin):
    form = CustomUserAdminForm
    
    # Adiciona os campos personalizados aos campos do admin
    fieldsets = UserAdmin.fieldsets + (
        (_('Informações Personalizadas'), {
            'fields': ('filha_nome', 'email_confirmed', 'is_admin'),
            'description': 'Informações específicas do sistema M_inha'
        }),
        (_('Texto de Início'), {
            'fields': ('texto_inicio',),
            'description': 'Texto personalizado exibido na tela inicial do usuário'
        }),
    )
    
    # Adiciona campos personalizados à lista de campos exibidos
    list_display = UserAdmin.list_display + ('filha_nome', 'email_confirmed', 'is_admin', 'tem_texto_inicio')
    
    # Adiciona filtros
    list_filter = UserAdmin.list_filter + ('is_admin', 'email_confirmed')
    
    # Permite buscar por filha_nome
    search_fields = UserAdmin.search_fields + ('filha_nome',)
    
    def tem_texto_inicio(self, obj):
        return bool(obj.texto_inicio)
    tem_texto_inicio.boolean = True
    tem_texto_inicio.short_description = 'Tem Texto de Início'

# Registra os modelos
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Historia)
admin.site.register(ItemHistoria)
