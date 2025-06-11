# Projeto M_inha

Sistema para criação e gerenciamento de histórias personalizadas com funcionalidades administrativas avançadas.

## 🚀 Como executar

### Opção 1: Script Automático (Recomendado)
```bash
./start_project.sh
```

### Opção 2: Manual
1. Ative o ambiente virtual:
```bash
source venv/bin/activate
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute as migrações:
```bash
python manage.py migrate
```

4. Execute o servidor de desenvolvimento:
```bash
python manage.py runserver 0.0.0.0:8002
```

5. Acesse http://localhost:8002 no seu navegador

## 📁 Estrutura do Projeto

- `M_inha/` - Diretório principal do projeto Django
- `accounts/` - App principal com modelos de usuário e funcionalidades
- `templates/` - Templates HTML
- `static/` - Arquivos estáticos (CSS, JS, imagens)
- `media/` - Arquivos de upload
- `venv/` - Ambiente virtual Python
- `manage.py` - Script de gerenciamento do Django
- `requirements.txt` - Dependências do projeto
- `start_project.sh` - Script para iniciar o projeto

---

# 👑 Sistema de Administrador

Este projeto implementa um sistema completo de diferenciação entre usuários administradores e usuários comuns, com funcionalidades avançadas de gerenciamento.

## 🎯 Funcionalidades Implementadas

### Para Administradores
- ✅ **Badge Visual**: Identificação clara na interface com badge amarelo
- ✅ **Menu Exclusivo**: Seção administrativa na sidebar
- ✅ **Dashboard Administrativo**: Estatísticas completas do sistema
- ✅ **Gerenciamento de Usuários**: Promover/rebaixar usuários
- ✅ **Acesso Ampliado**: Acesso a todas as funcionalidades do sistema
- ✅ **Feedback Visual**: Mensagens de confirmação para todas as ações

### Para Usuários Comuns
- ✅ **Acesso Controlado**: Acesso apenas às funcionalidades básicas
- ✅ **Redirecionamento Inteligente**: Mensagens amigáveis para acesso negado
- ✅ **Interface Limpa**: Sem opções administrativas desnecessárias

## 🛠️ Comandos de Gerenciamento

### Criar Novo Administrador
```bash
# Modo interativo (recomendado)
python manage.py create_admin

# Com parâmetros (não recomendado para produção)
python manage.py create_admin --email admin@exemplo.com --username admin --filha-nome "Nome da Filha"
```

### Promover Usuário Existente
```bash
# Promover para administrador
python manage.py promote_admin usuario@email.com

# Rebaixar para usuário comum
python manage.py promote_admin usuario@email.com --demote
```

## 🔐 Sistema de Segurança

### Decorators Disponíveis

#### `@admin_required`
```python
from accounts.decorators import admin_required

@admin_required
def minha_view_restrita(request):
    # Somente administradores podem acessar
    return render(request, 'template.html')
```

#### `@admin_required_message`
```python
from accounts.decorators import admin_required_message

@admin_required_message
def outra_view_restrita(request):
    # Redireciona com mensagem amigável se não for admin
    return render(request, 'template.html')
```

#### Função Helper
```python
from accounts.decorators import is_admin_or_owner

def minha_view(request):
    obj = MinhaModel.objects.get(pk=1)
    if is_admin_or_owner(request.user, obj):
        # Usuário é admin ou dono do objeto
        pass
```

### Template Tags Personalizados

#### Carregamento
```html
{% load admin_tags %}
```

#### Verificação de Administrador
```html
{% if user|is_admin %}
    <p>Você é administrador!</p>
{% endif %}
```

#### Tipo de Usuário
```html
<p>Tipo: {{ user|user_type }}</p>
<!-- Output: "Administrador" ou "Usuário Comum" -->
```

#### Badge de Administrador
```html
{% show_admin_badge user %}
<!-- Mostra badge automaticamente se for admin -->
```

#### Verificação Avançada
```html
{% can_access_admin_area user as can_access %}
{% if can_access %}
    <a href="{% url 'admin_dashboard' %}">Área Admin</a>
{% endif %}
```

## 🌐 URLs Administrativas

| URL | Nome | Descrição | Acesso |
|-----|------|-----------|--------|
| `/admin-dashboard/` | `admin_dashboard` | Dashboard com estatísticas | Somente Admin |
| `/manage-users/` | `manage_users` | Gerenciar usuários | Somente Admin |
| `/admin/` | - | Admin Django nativo | Staff/Superuser |

## 💾 Modelo de Dados

### Campo Adicional no CustomUser
```python
class CustomUser(AbstractUser):
    # ... outros campos ...
    is_admin = models.BooleanField(
        _('é administrador'), 
        default=False, 
        help_text=_('Determina se o usuário tem privilégios de administrador.')
    )
```

### Métodos Úteis
```python
user = CustomUser.objects.get(email='teste@exemplo.com')

# Verificar se é administrador
if user.is_administrator():
    print("É administrador!")

# Obter tipo de usuário
print(user.get_user_type())  # "Administrador" ou "Usuário Comum"
```

## 🎨 Interface do Usuário

### Elementos Visuais

#### Badge de Administrador
- **Cor**: Amarelo com texto escuro
- **Ícone**: `bi-shield-check`
- **Localização**: Navbar superior, listas de usuários

#### Menu Administrativo
- **Separador**: Linha divisória na sidebar
- **Ícones**: Shield para dashboard, People para usuários
- **Visibilidade**: Apenas para administradores

### Páginas Administrativas

#### Dashboard (`/admin-dashboard/`)
- **Estatísticas**: Total de usuários, admins, histórias, itens
- **Usuários Recentes**: Lista dos 5 usuários mais recentes
- **Ações Rápidas**: Links para funcionalidades importantes

#### Gerenciar Usuários (`/manage-users/`)
- **Tabela Completa**: Todos os dados dos usuários
- **Ações**: Promover/Rebaixar com confirmação
- **Informações**: Status de confirmação de email, tipo de usuário
- **Segurança**: Não permite auto-rebaixamento

## 📋 Exemplos Práticos

### 1. Criando uma View Administrativa
```python
from accounts.decorators import admin_required_message

@admin_required_message
def relatorios_avancados(request):
    """View que só administradores podem acessar"""
    dados = MinhaModel.objects.aggregate(
        total=Count('id'),
        media=Avg('campo_numerico')
    )
    return render(request, 'relatorios.html', {'dados': dados})
```

### 2. Template com Lógica Administrativa
```html
{% extends 'base.html' %}
{% load admin_tags %}

{% block content %}
<h1>Minha Página</h1>

{% if user|is_admin %}
    <div class="alert alert-warning">
        <strong>Modo Administrador:</strong> Você tem acesso completo.
    </div>
    
    <a href="{% url 'manage_users' %}" class="btn btn-primary">
        Gerenciar Usuários
    </a>
{% endif %}

<p>Seu tipo: {{ user|user_type }}</p>
{% endblock %}
```

### 3. Verificação em Views Existentes
```python
def editar_historia(request, historia_id):
    historia = get_object_or_404(Historia, id=historia_id)
    
    # Admin pode editar qualquer história, user só a própria
    if not (request.user.is_admin or historia.usuario == request.user):
        messages.error(request, 'Você não tem permissão para editar esta história.')
        return redirect('historias')
    
    # ... resto da lógica
```

## 🔧 Configuração no Admin Django

O modelo `CustomUser` está registrado no admin Django com campos personalizados:

```python
# admin.py
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (_('Informações Personalizadas'), {
            'fields': ('filha_nome', 'email_confirmed', 'is_admin')
        }),
    )
    list_display = UserAdmin.list_display + ('filha_nome', 'email_confirmed', 'is_admin')
    list_filter = UserAdmin.list_filter + ('is_admin', 'email_confirmed')
```

## 🚨 Considerações de Segurança

1. **Não Auto-Rebaixamento**: Administradores não podem remover seus próprios privilégios
2. **Verificação Dupla**: Todas as views administrativas têm decorators de segurança
3. **Template Protection**: Template tags impedem exibição de conteúdo não autorizado
4. **Feedback Claro**: Mensagens informativas para tentativas de acesso negado
5. **Logs Implícitos**: Django registra automaticamente ações administrativas

## 🧪 Como Testar

### 1. Configuração Inicial
```bash
# 1. Execute as migrações (se ainda não executou)
python manage.py migrate

# 2. Crie um administrador
python manage.py create_admin

# 3. Inicie o servidor
./start_project.sh
```

### 2. Testes de Funcionalidade
1. **Login como Admin**: Verifique badge e menu exclusivo
2. **Dashboard**: Acesse `/admin-dashboard/` e verifique estatísticas
3. **Gerenciar Usuários**: Acesse `/manage-users/` e teste promoção/rebaixamento
4. **Login como Usuário Comum**: Confirme que não vê opções administrativas
5. **Teste de Segurança**: Tente acessar URLs admin como usuário comum

### 3. Validação de Templates
- Badge aparece na navbar para admins
- Menu administrativo visível apenas para admins
- Mensagens de feedback funcionando
- Redirecionamentos de segurança operando

## 📚 Arquivos Criados/Modificados

### Novos Arquivos
- `accounts/decorators.py` - Decorators de segurança
- `accounts/templatetags/admin_tags.py` - Template tags personalizados
- `accounts/management/commands/create_admin.py` - Comando para criar admin
- `accounts/management/commands/promote_admin.py` - Comando para promover usuário
- `templates/accounts/admin_dashboard.html` - Dashboard administrativo
- `templates/accounts/manage_users.html` - Gerenciar usuários
- `templates/accounts/admin_badge.html` - Badge de administrador

### Arquivos Modificados
- `accounts/models.py` - Adicionado campo `is_admin`
- `accounts/admin.py` - Configuração do admin Django
- `accounts/views.py` - Adicionadas views administrativas
- `accounts/urls.py` - Adicionadas rotas administrativas
- `templates/base.html` - Menu e badge administrativo

---

## 💡 Dicas de Uso

1. **Primeiro Admin**: Sempre crie pelo menos um administrador usando `python manage.py create_admin`
2. **Backup de Admins**: Mantenha sempre pelo menos 2 administradores ativos
3. **Testes**: Use contas separadas para testar funcionalidades de usuário comum
4. **Customização**: Os templates podem ser facilmente customizados para sua marca
5. **Monitoramento**: Use o dashboard para acompanhar o crescimento da plataforma

---

*Documentação atualizada em: {{ "now"|date:"d/m/Y" }}*

# El Oso y la Pata 🐻🦆

Sistema de histórias personalizadas construído com Django.

## 🚀 Deploy no Railway

### Pré-requisitos
1. Conta no GitHub
2. Conta no Railway
3. Projeto commitado no GitHub

### Passo a Passo

1. **Push para GitHub**
   ```bash
   git add .
   git commit -m "Preparação para produção"
   git push
   ```

2. **Deploy no Railway**
   - Acesse [railway.app](https://railway.app)
   - Clique em "Deploy from GitHub repo"
   - Selecione este repositório
   - Railway detectará automaticamente que é Django

3. **Configurar Variáveis de Ambiente**
   No Railway, adicione:
   ```
   DEBUG=False
   SECRET_KEY=sua-chave-super-secreta-aqui
   ALLOWED_HOSTS=seu-dominio.railway.app
   ADMIN_USERNAME=admin
   ADMIN_EMAIL=admin@example.com
   ADMIN_PASSWORD=senha-super-segura
   ADMIN_FILHA_NOME=Sofia
   ```

4. **Banco de Dados**
   - Railway criará automaticamente PostgreSQL
   - A variável `DATABASE_URL` será configurada automaticamente

### 🎯 Após Deploy

O sistema criará automaticamente um usuário administrador com as credenciais configuradas.

### 📁 Estrutura

```
├── accounts/          # App principal
├── templates/         # Templates HTML
├── static/           # Arquivos estáticos
├── M_inha/           # Configurações Django
├── Procfile          # Configuração Railway
├── requirements.txt  # Dependências Python
└── runtime.txt       # Versão Python
```

### 🔧 Desenvolvimento Local

1. Clone o projeto
2. Crie ambiente virtual: `python -m venv venv`
3. Ative: `source venv/bin/activate` (Linux/Mac) ou `venv\Scripts\activate` (Windows)
4. Instale: `pip install -r requirements.txt`
5. Execute: `python manage.py runserver`

### 📝 Recursos

- ✅ Sistema de usuários customizado
- ✅ Histórias com upload de imagens
- ✅ Slideshow de visualização
- ✅ Painel administrativo
- ✅ Gestão de usuários
- ✅ Interface responsiva 