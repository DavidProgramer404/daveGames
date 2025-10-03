#!/usr/bin/env python
"""
Script para configurar variables de entorno en Vercel
DaveGames - Portal de Juegos
"""

import subprocess
import secrets
import string

def generate_secret_key():
    """Generar una clave secreta segura para Django"""
    chars = string.ascii_letters + string.digits + '!@#$%^&*(-_=+)'
    return ''.join(secrets.choice(chars) for _ in range(50))

def set_vercel_env(key, value, environment='production'):
    """Configurar variable de entorno en Vercel"""
    try:
        cmd = ['vercel', 'env', 'add', key, environment]
        result = subprocess.run(cmd, input=value, text=True, capture_output=True)
        
        if result.returncode == 0:
            print(f"✅ {key} configurado en {environment}")
            return True
        else:
            print(f"❌ Error configurando {key}: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("🔧 DaveGames - Configuración de Variables de Entorno en Vercel")
    print("=" * 60)
    
    # Variables de entorno necesarias
    env_vars = {
        'SECRET_KEY': generate_secret_key(),
        'DEBUG': 'False',
        'ALLOWED_HOSTS': 'dave-games-jz9mac46j-davidprogramer404s-projects.vercel.app,.vercel.app',
        'DJANGO_SETTINGS_MODULE': 'davegames_project.settings'
    }
    
    print("📋 Variables a configurar:")
    for key, value in env_vars.items():
        if key == 'SECRET_KEY':
            print(f"   - {key}: [GENERADA AUTOMÁTICAMENTE]")
        else:
            print(f"   - {key}: {value}")
    
    response = input("\n¿Continuar con la configuración? (y/N): ").strip().lower()
    if response != 'y':
        print("❌ Configuración cancelada")
        return
    
    # Configurar variables
    success_count = 0
    for key, value in env_vars.items():
        if set_vercel_env(key, value):
            success_count += 1
    
    print(f"\n📊 Resultado: {success_count}/{len(env_vars)} variables configuradas")
    
    if success_count == len(env_vars):
        print("\n🎉 ¡Todas las variables configuradas exitosamente!")
        print("\n📋 Próximos pasos:")
        print("1. Configurar base de datos PostgreSQL en Vercel")
        print("2. Agregar DATABASE_URL como variable de entorno")
        print("3. Redesplegar: vercel --prod")
        print("4. Ejecutar migraciones")
    else:
        print("\n⚠️ Algunas variables no se configuraron correctamente")
        print("Revisar manualmente en: https://vercel.com/dashboard")

if __name__ == "__main__":
    main()