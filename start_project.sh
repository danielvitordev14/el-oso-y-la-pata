#!/bin/bash

# Script para iniciar o projeto Django na porta 8002
echo "🚀 Iniciando o projeto Django..."

# Verifica se existe ambiente virtual e ativa
if [ -d "venv" ]; then
    echo "📦 Ativando ambiente virtual..."
    source venv/bin/activate
else
    echo "⚠️  Ambiente virtual não encontrado. Criando um novo..."
    python3 -m venv venv
    source venv/bin/activate
fi

# Instala/atualiza dependências
echo "📚 Instalando dependências..."
pip install -r requirements.txt

# Executa migrações
echo "🔄 Executando migrações..."
python manage.py makemigrations
python manage.py migrate

# Coleta arquivos estáticos (se necessário)
echo "📁 Coletando arquivos estáticos..."
python manage.py collectstatic --noinput 2>/dev/null || echo "⚠️  Collectstatic não configurado ou falhou - continuando..."

# Inicia o servidor na porta 8002
echo "🌐 Iniciando servidor na porta 8002..."
echo "✅ Acesse o projeto em: http://localhost:8002"
echo "🛑 Para parar o servidor, pressione Ctrl+C"
python manage.py runserver 0.0.0.0:8002 