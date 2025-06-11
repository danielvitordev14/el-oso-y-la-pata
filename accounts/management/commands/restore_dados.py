from django.core.management.base import BaseCommand
from django.core.management import call_command
import os

class Command(BaseCommand):
    help = 'Restaura dados do backup JSON'

    def handle(self, *args, **options):
        backup_file = 'backup_dados.json'
        
        if os.path.exists(backup_file):
            self.stdout.write('Carregando dados do backup...')
            try:
                call_command('loaddata', backup_file)
                self.stdout.write(
                    self.style.SUCCESS('✅ Dados restaurados com sucesso!')
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'❌ Erro ao restaurar dados: {e}')
                )
        else:
            self.stdout.write(
                self.style.WARNING('⚠️ Arquivo backup_dados.json não encontrado')
            ) 