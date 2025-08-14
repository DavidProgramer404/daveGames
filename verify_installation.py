#!/usr/bin/env python
"""
Script de verificación de instalación para DaveGames
Verifica que todas las dependencias estén instaladas correctamente
"""

import sys
import subprocess
import importlib

def check_python_version():
    """Verificar versión de Python"""
    print("🐍 Verificando versión de Python...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor}.{version.micro} - Requiere Python 3.8+")
        return False

def check_package(package_name, import_name=None):
    """Verificar si un paquete está instalado"""
    if import_name is None:
        import_name = package_name
    
    try:
        module = importlib.import_module(import_name)
        if hasattr(module, '__version__'):
            version = module.__version__
        else:
            version = "instalado"
        print(f"   ✅ {package_name}: {version}")
        return True
    except ImportError:
        print(f"   ❌ {package_name}: No instalado")
        return False

def check_django_setup():
    """Verificar configuración de Django"""
    print("\n🔧 Verificando configuración de Django...")
    try:
        import os
        import django
        
        # Configurar Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'davegames_project.settings')
        django.setup()
        
        from django.conf import settings
        from django.db import connection
        
        print(f"   ✅ Django configurado correctamente")
        print(f"   ✅ Base de datos: {settings.DATABASES['default']['ENGINE']}")
        
        # Probar conexión a la base de datos
        try:
            connection.ensure_connection()
            print(f"   ✅ Conexión a base de datos: OK")
            return True
        except Exception as e:
            print(f"   ❌ Error de conexión a base de datos: {e}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error en configuración de Django: {e}")
        return False

def main():
    """Función principal de verificación"""
    print("🎮 DaveGames - Verificación de Instalación")
    print("=" * 50)
    
    all_ok = True
    
    # Verificar Python
    if not check_python_version():
        all_ok = False
    
    # Verificar paquetes principales
    print("\n📦 Verificando paquetes instalados...")
    packages = [
        ('Django', 'django'),
        ('Pillow', 'PIL'),
        ('psycopg2-binary', 'psycopg2'),
        ('asgiref', 'asgiref'),
        ('sqlparse', 'sqlparse'),
    ]
    
    for package_name, import_name in packages:
        if not check_package(package_name, import_name):
            all_ok = False
    
    # Verificar Django
    if not check_django_setup():
        all_ok = False
    
    # Verificar archivos del proyecto
    print("\n📁 Verificando archivos del proyecto...")
    required_files = [
        'manage.py',
        'requirements.txt',
        'davegames_project/settings.py',
        'games/models.py',
        'games/views.py',
        'games/admin.py',
    ]
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path} - No encontrado")
            all_ok = False
    
    # Resultado final
    print("\n" + "=" * 50)
    if all_ok:
        print("🎉 ¡Instalación verificada exitosamente!")
        print("\n📋 Próximos pasos:")
        print("   1. python manage.py migrate")
        print("   2. python manage.py createsuperuser")
        print("   3. python manage.py runserver")
        print("\n🌐 Acceder a: http://127.0.0.1:8000/")
    else:
        print("❌ Se encontraron problemas en la instalación")
        print("\n🔧 Para solucionarlos:")
        print("   1. pip install -r requirements.txt")
        print("   2. Verificar configuración de PostgreSQL")
        print("   3. Ejecutar este script nuevamente")
    
    return all_ok

if __name__ == "__main__":
    import os
    main()