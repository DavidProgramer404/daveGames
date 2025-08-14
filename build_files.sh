#!/bin/bash

# DaveGames - Script de construcción para Vercel
echo "🎮 Construyendo DaveGames para Vercel..."

# Instalar dependencias
echo "📦 Instalando dependencias..."
pip install -r requirements.txt

# Recopilar archivos estáticos
echo "📁 Recopilando archivos estáticos..."
python manage.py collectstatic --noinput --clear

# Crear directorio para archivos estáticos
mkdir -p staticfiles_build

# Copiar archivos estáticos
cp -r staticfiles/* staticfiles_build/

echo "✅ Construcción completada!"