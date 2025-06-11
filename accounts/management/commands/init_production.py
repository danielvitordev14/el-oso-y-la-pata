from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.conf import settings
import os

User = get_user_model()

class Command(BaseCommand):
    help = 'Inicializa ambiente de produção com usuário admin'

    def handle(self, *args, **options):
        # Verifica se já existe um superusuário
        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write(
                self.style.SUCCESS('Superusuário já existe!')
            )
            return

        # Pega credenciais do ambiente ou usa padrões
        username = os.environ.get('ADMIN_USERNAME', 'admin')
        email = os.environ.get('ADMIN_EMAIL', 'admin@elosoylaPata.com')
        password = os.environ.get('ADMIN_PASSWORD', 'admin123')
        filha_nome = os.environ.get('ADMIN_FILHA_NOME', 'Sofia')

        # Cria o superusuário
        admin_user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            filha_nome=filha_nome,
            is_admin=True,
            is_staff=True,
            is_superuser=True,
            email_confirmed=True
        )

        self.stdout.write(
            self.style.SUCCESS(
                f'Superusuário criado com sucesso!\n'
                f'Username: {username}\n'
                f'Email: {email}\n'
                f'Password: {password}\n'
                f'Filha: {filha_nome}'
            )
        ) 