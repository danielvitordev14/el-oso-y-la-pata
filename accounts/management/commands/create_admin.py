from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
import getpass

User = get_user_model()

class Command(BaseCommand):
    help = 'Cria um usuário administrador'

    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            type=str,
            help='Email do usuário administrador',
        )
        parser.add_argument(
            '--username',
            type=str,
            help='Nome de usuário',
        )
        parser.add_argument(
            '--filha-nome',
            type=str,
            help='Nome da filha',
        )
        parser.add_argument(
            '--password',
            type=str,
            help='Senha (não recomendado usar via linha de comando)',
        )
        parser.add_argument(
            '--texto-inicio',
            type=str,
            help='Texto personalizado para a tela inicial do usuário',
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('=== Criação de Usuário Administrador ===')
        )

        # Coleta informações do usuário
        email = options.get('email')
        if not email:
            email = input('Email: ')

        username = options.get('username')
        if not username:
            username = input('Nome de usuário: ')

        filha_nome = options.get('filha_nome')
        if not filha_nome:
            filha_nome = input('Nome da filha: ')

        texto_inicio = options.get('texto_inicio')
        if not texto_inicio:
            texto_inicio = input('Texto personalizado para tela inicial (opcional): ')

        password = options.get('password')
        if not password:
            password = getpass.getpass('Senha: ')
            password_confirm = getpass.getpass('Confirme a senha: ')
            
            if password != password_confirm:
                self.stdout.write(
                    self.style.ERROR('As senhas não coincidem!')
                )
                return

        # Verifica se o email já existe
        if User.objects.filter(email=email).exists():
            self.stdout.write(
                self.style.ERROR(f'Usuário com email {email} já existe!')
            )
            return

        # Verifica se o username já existe
        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.ERROR(f'Usuário com username {username} já existe!')
            )
            return

        try:
            # Cria o usuário administrador
            user = User.objects.create_user(
                email=email,
                username=username,
                password=password,
                filha_nome=filha_nome,
                is_admin=True,
                is_staff=True,
                is_superuser=True,
                email_confirmed=True,
                texto_inicio=texto_inicio if texto_inicio else None
            )

            self.stdout.write(
                self.style.SUCCESS(
                    f'Usuário administrador {username} ({email}) criado com sucesso!'
                )
            )
            
            self.stdout.write(
                self.style.WARNING(
                    'Características do usuário:'
                )
            )
            self.stdout.write(f'  - Email: {user.email}')
            self.stdout.write(f'  - Username: {user.username}')
            self.stdout.write(f'  - Nome da filha: {user.filha_nome}')
            self.stdout.write(f'  - Texto de início: {user.texto_inicio or "Não configurado"}')
            self.stdout.write(f'  - É administrador: {user.is_admin}')
            self.stdout.write(f'  - É staff: {user.is_staff}')
            self.stdout.write(f'  - É superuser: {user.is_superuser}')

        except ValidationError as e:
            self.stdout.write(
                self.style.ERROR(f'Erro de validação: {e}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Erro inesperado: {e}')
            ) 