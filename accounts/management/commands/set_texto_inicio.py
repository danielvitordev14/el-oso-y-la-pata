from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Define o texto de início para um usuário existente'

    def add_arguments(self, parser):
        parser.add_argument(
            'email',
            type=str,
            help='Email do usuário',
        )
        parser.add_argument(
            'texto',
            type=str,
            help='Texto de início a ser definido',
        )

    def handle(self, *args, **options):
        email = options['email']
        texto = options['texto']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'Usuário com email {email} não encontrado!')
            )
            return

        user.texto_inicio = texto
        user.save()

        self.stdout.write(
            self.style.SUCCESS(
                f'Texto de início atualizado para {user.username} ({email})!'
            )
        )
        
        self.stdout.write(
            self.style.WARNING('Texto definido:')
        )
        self.stdout.write(f'"{texto}"') 