#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'M_inha.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

# Testar Cloudinary
import cloudinary
import cloudinary.uploader
from django.conf import settings

print("=== TESTE CLOUDINARY ===")
print(f"Cloud Name: {settings.CLOUDINARY_STORAGE['CLOUD_NAME']}")
print(f"API Key: {settings.CLOUDINARY_STORAGE['API_KEY']}")
print(f"DEFAULT_FILE_STORAGE: {getattr(settings, 'DEFAULT_FILE_STORAGE', 'Não definido')}")

# Tentar fazer upload de teste
try:
    # Usar a logo como teste
    logo_path = os.path.join(settings.BASE_DIR, 'static', 'img', 'logo.png')
    if os.path.exists(logo_path):
        print(f"\nTentando upload do arquivo: {logo_path}")
        result = cloudinary.uploader.upload(logo_path, folder="test")
        print(f"✅ Upload realizado com sucesso!")
        print(f"URL: {result['url']}")
        print(f"Secure URL: {result['secure_url']}")
    else:
        print(f"❌ Arquivo não encontrado: {logo_path}")
        
except Exception as e:
    print(f"❌ Erro no upload: {e}")
    
print("\n=== FIM DO TESTE ===") 