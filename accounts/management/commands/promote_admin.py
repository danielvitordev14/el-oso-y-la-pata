from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Promove um usuário existente a administrador'

    def add_arguments(self, parser):
        parser.add_argument(
            'email',
            type=str,
            help='Email do usuário a ser promovido',
        )
        parser.add_argument(
            '--demote',
            action='store_true',
            help='Remove privilégios de administrador ao invés de conceder',
        )

    def handle(self, *args, **options):
        email = options['email']
        demote = options.get('demote', False)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'Usuário com email {email} não encontrado!')
            )
            return

        if demote:
            # Remove privilégios de admin
            user.is_admin = False
            user.is_staff = False
            user.is_superuser = False
            user.save()
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Usuário {user.username} ({email}) foi rebaixado para usuário comum!'
                )
            )
        else:
            # Concede privilégios de admin
            user.is_admin = True
            user.is_staff = True
            user.is_superuser = True
            user.save()
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Usuário {user.username} ({email}) foi promovido a administrador!'
                )
            )

        # Mostra status atual
        self.stdout.write(
            self.style.WARNING('Status atual do usuário:')
        )
        self.stdout.write(f'  - Email: {user.email}')
        self.stdout.write(f'  - Username: {user.username}')
        self.stdout.write(f'  - É administrador: {user.is_admin}')
        self.stdout.write(f'  - É staff: {user.is_staff}')
        self.stdout.write(f'  - É superuser: {user.is_superuser}') 