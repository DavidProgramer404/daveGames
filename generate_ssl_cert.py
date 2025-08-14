#!/usr/bin/env python
"""
Script para generar certificados SSL self-signed para desarrollo local
DaveGames - Portal de Juegos
"""

import os
import subprocess
import sys
from datetime import datetime, timedelta

def check_openssl():
    """Verificar si OpenSSL está disponible"""
    try:
        subprocess.run(['openssl', 'version'], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def generate_ssl_certificate():
    """Generar certificado SSL self-signed"""
    print("🔒 DaveGames - Generador de Certificados SSL")
    print("=" * 50)
    
    # Verificar OpenSSL
    if not check_openssl():
        print("❌ OpenSSL no está instalado o no está en el PATH")
        print("\n📋 Instrucciones de instalación:")
        print("Windows: Descargar desde https://slproweb.com/products/Win32OpenSSL.html")
        print("macOS: brew install openssl")
        print("Ubuntu/Debian: sudo apt-get install openssl")
        return False
    
    print("✅ OpenSSL encontrado")
    
    # Configuración del certificado
    cert_config = {
        'country': 'ES',
        'state': 'Madrid',
        'city': 'Madrid',
        'organization': 'DaveGames',
        'organizational_unit': 'Development',
        'common_name': 'localhost',
        'email': 'admin@davegames.local'
    }
    
    # Archivos de salida
    key_file = 'davegames_ssl.key'
    cert_file = 'davegames_ssl.crt'
    
    # Verificar si ya existen
    if os.path.exists(key_file) and os.path.exists(cert_file):
        response = input(f"⚠️  Los archivos {key_file} y {cert_file} ya existen. ¿Sobrescribir? (y/N): ")
        if response.lower() != 'y':
            print("❌ Operación cancelada")
            return False
    
    print("\n🔧 Generando certificado SSL...")
    
    # Crear subject string
    subject = f"/C={cert_config['country']}/ST={cert_config['state']}/L={cert_config['city']}/O={cert_config['organization']}/OU={cert_config['organizational_unit']}/CN={cert_config['common_name']}/emailAddress={cert_config['email']}"
    
    try:
        # Generar clave privada
        print("🔑 Generando clave privada...")
        subprocess.run([
            'openssl', 'genrsa', 
            '-out', key_file, 
            '2048'
        ], check=True, capture_output=True)
        
        # Generar certificado
        print("📜 Generando certificado...")
        subprocess.run([
            'openssl', 'req', 
            '-new', '-x509', 
            '-key', key_file, 
            '-out', cert_file, 
            '-days', '365',
            '-subj', subject
        ], check=True, capture_output=True)
        
        print("✅ Certificado SSL generado exitosamente!")
        print(f"📁 Archivos creados:")
        print(f"   - Clave privada: {key_file}")
        print(f"   - Certificado: {cert_file}")
        
        # Mostrar información del certificado
        print("\n📋 Información del certificado:")
        result = subprocess.run([
            'openssl', 'x509', 
            '-in', cert_file, 
            '-text', '-noout'
        ], capture_output=True, text=True)
        
        # Extraer fechas de validez
        lines = result.stdout.split('\n')
        for line in lines:
            if 'Not Before:' in line or 'Not After:' in line:
                print(f"   {line.strip()}")
        
        print(f"\n🚀 Para usar el certificado:")
        print(f"   1. Instalar django-extensions: pip install django-extensions Werkzeug pyOpenSSL")
        print(f"   2. Ejecutar: python manage.py runserver_plus --cert-file {cert_file} --key-file {key_file}")
        print(f"   3. Acceder a: https://localhost:8000")
        print(f"\n⚠️  Nota: El navegador mostrará una advertencia de seguridad.")
        print(f"   Esto es normal para certificados self-signed. Hacer clic en 'Avanzado' > 'Continuar'")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al generar certificado: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def create_ssl_config_file():
    """Crear archivo de configuración SSL para OpenSSL"""
    config_content = """
[req]
distinguished_name = req_distinguished_name
x509_extensions = v3_req
prompt = no

[req_distinguished_name]
C = ES
ST = Madrid
L = Madrid
O = DaveGames
OU = Development
CN = localhost
emailAddress = admin@davegames.local

[v3_req]
keyUsage = keyEncipherment, dataEncipherment
extendedKeyUsage = serverAuth
subjectAltName = @alt_names

[alt_names]
DNS.1 = localhost
DNS.2 = 127.0.0.1
DNS.3 = davegames.local
IP.1 = 127.0.0.1
IP.2 = ::1
"""
    
    with open('ssl_config.conf', 'w') as f:
        f.write(config_content.strip())
    
    return 'ssl_config.conf'

def generate_advanced_certificate():
    """Generar certificado con configuración avanzada"""
    print("\n🔧 Generando certificado avanzado con SAN...")
    
    config_file = create_ssl_config_file()
    key_file = 'davegames_ssl_advanced.key'
    cert_file = 'davegames_ssl_advanced.crt'
    
    try:
        # Generar clave privada
        subprocess.run([
            'openssl', 'genrsa', 
            '-out', key_file, 
            '2048'
        ], check=True, capture_output=True)
        
        # Generar certificado con configuración
        subprocess.run([
            'openssl', 'req', 
            '-new', '-x509', 
            '-key', key_file, 
            '-out', cert_file, 
            '-days', '365',
            '-config', config_file,
            '-extensions', 'v3_req'
        ], check=True, capture_output=True)
        
        print("✅ Certificado avanzado generado!")
        print(f"📁 Archivos:")
        print(f"   - {key_file}")
        print(f"   - {cert_file}")
        
        # Limpiar archivo de configuración
        os.remove(config_file)
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Función principal"""
    print("🎮 DaveGames SSL Certificate Generator")
    print("=" * 40)
    print("1. Certificado básico")
    print("2. Certificado avanzado (con SAN)")
    print("3. Salir")
    
    choice = input("\nSelecciona una opción (1-3): ").strip()
    
    if choice == '1':
        generate_ssl_certificate()
    elif choice == '2':
        generate_advanced_certificate()
    elif choice == '3':
        print("👋 ¡Hasta luego!")
        sys.exit(0)
    else:
        print("❌ Opción inválida")
        main()

if __name__ == "__main__":
    main()