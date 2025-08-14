#!/usr/bin/env python
"""
Script de despliegue automático para Vercel
DaveGames - Portal de Juegos
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def print_header():
    print("🚀 DaveGames - Despliegue en Vercel")
    print("=" * 40)

def check_vercel_cli():
    """Verificar si Vercel CLI está instalado"""
    try:
        result = subprocess.run(['vercel', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Vercel CLI: {result.stdout.strip()}")
            return True
        else:
            print("❌ Vercel CLI no encontrado")
            return False
    except FileNotFoundError:
        print("❌ Vercel CLI no está instalado")
        print("📋 Instalar con: npm i -g vercel")
        return False

def check_required_files():
    """Verificar archivos necesarios para Vercel"""
    required_files = [
        'vercel.json',
        'build_files.sh',
        'vercel_settings.py',
        'requirements_vercel.txt',
        'davegames_project/wsgi.py'
    ]
    
    print("\n📁 Verificando archivos necesarios...")
    all_present = True
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path} - No encontrado")
            all_present = False
    
    return all_present

def setup_environment():
    """Configurar entorno para Vercel"""
    print("\n🔧 Configurando entorno...")
    
    # Hacer ejecutable el script de construcción
    if os.path.exists('build_files.sh'):
        try:
            os.chmod('build_files.sh', 0o755)
            print("   ✅ build_files.sh hecho ejecutable")
        except Exception as e:
            print(f"   ⚠️  No se pudo hacer ejecutable build_files.sh: {e}")
    
    # Verificar requirements_vercel.txt
    if os.path.exists('requirements_vercel.txt'):
        print("   ✅ requirements_vercel.txt encontrado")
    else:
        print("   ❌ requirements_vercel.txt no encontrado")
        return False
    
    return True

def collect_static_files():
    """Recopilar archivos estáticos"""
    print("\n📦 Recopilando archivos estáticos...")
    
    try:
        # Configurar Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vercel_settings')
        
        # Ejecutar collectstatic
        result = subprocess.run([
            sys.executable, 'manage.py', 'collectstatic', '--noinput', '--clear'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("   ✅ Archivos estáticos recopilados")
            return True
        else:
            print(f"   ❌ Error recopilando archivos estáticos: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def configure_vercel_project():
    """Configurar proyecto en Vercel"""
    print("\n⚙️  Configurando proyecto Vercel...")
    
    # Verificar si ya está configurado
    if os.path.exists('.vercel'):
        print("   ✅ Proyecto ya configurado")
        return True
    
    try:
        # Inicializar proyecto
        result = subprocess.run(['vercel'], input='y\n', text=True, capture_output=True)
        
        if result.returncode == 0:
            print("   ✅ Proyecto configurado en Vercel")
            return True
        else:
            print(f"   ❌ Error configurando proyecto: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def set_environment_variables():
    """Configurar variables de entorno en Vercel"""
    print("\n🔐 Configurando variables de entorno...")
    
    env_vars = {
        'DJANGO_SETTINGS_MODULE': 'vercel_settings',
        'DEBUG': 'False',
        'SECRET_KEY': 'django-insecure-change-this-in-production-vercel-key-12345',
    }
    
    for key, value in env_vars.items():
        try:
            result = subprocess.run([
                'vercel', 'env', 'add', key
            ], input=f"{value}\n", text=True, capture_output=True)
            
            if result.returncode == 0:
                print(f"   ✅ {key} configurado")
            else:
                print(f"   ⚠️  {key} - {result.stderr.strip()}")
                
        except Exception as e:
            print(f"   ❌ Error configurando {key}: {e}")
    
    print("\n⚠️  IMPORTANTE: Configurar manualmente en Vercel Dashboard:")
    print("   - SECRET_KEY: Generar clave segura de 50+ caracteres")
    print("   - DATABASE_URL: URL de PostgreSQL")
    print("   - Visitar: https://vercel.com/dashboard")

def deploy_to_vercel():
    """Desplegar a Vercel"""
    print("\n🚀 Desplegando a Vercel...")
    
    try:
        result = subprocess.run(['vercel', '--prod'], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("   ✅ Despliegue exitoso!")
            
            # Extraer URL del output
            lines = result.stdout.split('\n')
            for line in lines:
                if 'https://' in line and 'vercel.app' in line:
                    url = line.strip()
                    print(f"   🌐 URL: {url}")
                    break
            
            return True
        else:
            print(f"   ❌ Error en despliegue: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def show_post_deployment_steps():
    """Mostrar pasos post-despliegue"""
    print("\n📋 Pasos post-despliegue:")
    print("1. 🔐 Configurar variables de entorno en Vercel Dashboard")
    print("2. 🗄️  Configurar base de datos PostgreSQL")
    print("3. 🔄 Ejecutar migraciones (si es necesario)")
    print("4. 👤 Crear superusuario")
    print("5. 🔍 Verificar SSL con: python test_ssl.py https://tu-app.vercel.app")
    
    print("\n🔗 Enlaces útiles:")
    print("   - Dashboard: https://vercel.com/dashboard")
    print("   - Docs: https://vercel.com/docs")
    print("   - PostgreSQL: https://vercel.com/docs/storage/vercel-postgres")

def main():
    """Función principal"""
    print_header()
    
    # Verificaciones previas
    if not check_vercel_cli():
        return False
    
    if not check_required_files():
        print("\n❌ Faltan archivos necesarios. Ejecutar primero la configuración SSL.")
        return False
    
    if not setup_environment():
        return False
    
    # Preguntar al usuario si continuar
    response = input("\n¿Continuar con el despliegue? (y/N): ").strip().lower()
    if response != 'y':
        print("❌ Despliegue cancelado")
        return False
    
    # Proceso de despliegue
    steps = [
        ("Recopilar archivos estáticos", collect_static_files),
        ("Configurar proyecto Vercel", configure_vercel_project),
        ("Configurar variables de entorno", set_environment_variables),
        ("Desplegar a Vercel", deploy_to_vercel),
    ]
    
    for step_name, step_function in steps:
        print(f"\n🔄 {step_name}...")
        if not step_function():
            print(f"❌ Falló: {step_name}")
            return False
    
    # Mostrar pasos finales
    show_post_deployment_steps()
    
    print("\n🎉 ¡Despliegue completado!")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)