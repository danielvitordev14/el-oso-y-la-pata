#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'M_inha.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.conf import settings

print("=== DEBUG CLOUDINARY ===")
print(f"DEFAULT_FILE_STORAGE: {getattr(settings, 'DEFAULT_FILE_STORAGE', 'NÃO DEFINIDO')}")

try:
    print(f"CLOUDINARY_STORAGE: {settings.CLOUDINARY_STORAGE}")
except Exception as e:
    print(f"❌ Erro ao acessar CLOUDINARY_STORAGE: {e}")

try:
    import cloudinary
    print(f"✅ Cloudinary importado com sucesso")
    print(f"Cloudinary config: {cloudinary.config()}")
except ImportError as e:
    print(f"❌ Erro ao importar cloudinary: {e}")
except Exception as e:
    print(f"❌ Erro na configuração do cloudinary: {e}")

try:
    import cloudinary_storage
    print(f"✅ Cloudinary storage importado")
except ImportError as e:
    print(f"❌ Erro ao importar cloudinary_storage: {e}")

# Testar se as variáveis estão carregadas
cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME')
api_key = os.environ.get('CLOUDINARY_API_KEY')
api_secret = os.environ.get('CLOUDINARY_API_SECRET')

print(f"\nVariáveis de ambiente:")
print(f"CLOUDINARY_CLOUD_NAME: {'✅ ' + cloud_name if cloud_name else '❌ NÃO ENCONTRADA'}")
print(f"CLOUDINARY_API_KEY: {'✅ ' + api_key if api_key else '❌ NÃO ENCONTRADA'}")
print(f"CLOUDINARY_API_SECRET: {'✅ DEFINIDA' if api_secret else '❌ NÃO ENCONTRADA'}")

print("\n=== FIM DEBUG ===") 