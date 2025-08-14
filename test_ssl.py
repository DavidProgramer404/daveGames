#!/usr/bin/env python
"""
Script de prueba SSL para DaveGames
Verifica configuraciones SSL y conexiones HTTPS
"""

import os
import sys
import ssl
import socket
import urllib.request
import urllib.error
from urllib.parse import urlparse

def test_ssl_connection(url):
    """Probar conexión SSL a una URL"""
    print(f"🔍 Probando conexión SSL a: {url}")
    
    try:
        parsed_url = urlparse(url)
        hostname = parsed_url.hostname
        port = parsed_url.port or (443 if parsed_url.scheme == 'https' else 80)
        
        # Crear contexto SSL
        context = ssl.create_default_context()
        
        # Conectar
        with socket.create_connection((hostname, port), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                print(f"   ✅ Conexión SSL exitosa")
                print(f"   📜 Protocolo: {ssock.version()}")
                print(f"   🔐 Cifrado: {ssock.cipher()}")
                
                # Información del certificado
                cert = ssock.getpeercert()
                print(f"   📋 Certificado:")
                print(f"      - Emisor: {dict(x[0] for x in cert['issuer'])}")
                print(f"      - Sujeto: {dict(x[0] for x in cert['subject'])}")
                print(f"      - Válido desde: {cert['notBefore']}")
                print(f"      - Válido hasta: {cert['notAfter']}")
                
                return True
                
    except Exception as e:
        print(f"   ❌ Error de conexión SSL: {e}")
        return False

def test_http_request(url):
    """Probar petición HTTP/HTTPS"""
    print(f"\n🌐 Probando petición HTTP a: {url}")
    
    try:
        # Crear request con headers
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'DaveGames SSL Tester/1.0')
        
        with urllib.request.urlopen(req, timeout=10) as response:
            print(f"   ✅ Respuesta HTTP: {response.status} {response.reason}")
            
            # Verificar headers de seguridad
            headers = dict(response.headers)
            security_headers = [
                'Strict-Transport-Security',
                'X-Frame-Options',
                'X-Content-Type-Options',
                'X-XSS-Protection',
                'Content-Security-Policy'
            ]
            
            print(f"   🔒 Headers de seguridad:")
            for header in security_headers:
                value = headers.get(header, 'No configurado')
                status = "✅" if value != 'No configurado' else "⚠️"
                print(f"      {status} {header}: {value}")
            
            return True
            
    except urllib.error.HTTPError as e:
        print(f"   ❌ Error HTTP: {e.code} {e.reason}")
        return False
    except Exception as e:
        print(f"   ❌ Error de petición: {e}")
        return False

def test_django_ssl_settings():
    """Probar configuraciones SSL de Django"""
    print(f"\n🔧 Verificando configuraciones SSL de Django...")
    
    try:
        # Configurar Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'davegames_project.settings')
        import django
        django.setup()
        
        from django.conf import settings
        
        # Verificar configuraciones SSL
        ssl_settings = {
            'SECURE_SSL_REDIRECT': getattr(settings, 'SECURE_SSL_REDIRECT', False),
            'SESSION_COOKIE_SECURE': getattr(settings, 'SESSION_COOKIE_SECURE', False),
            'CSRF_COOKIE_SECURE': getattr(settings, 'CSRF_COOKIE_SECURE', False),
            'SECURE_HSTS_SECONDS': getattr(settings, 'SECURE_HSTS_SECONDS', 0),
            'SECURE_HSTS_INCLUDE_SUBDOMAINS': getattr(settings, 'SECURE_HSTS_INCLUDE_SUBDOMAINS', False),
            'SECURE_HSTS_PRELOAD': getattr(settings, 'SECURE_HSTS_PRELOAD', False),
            'SECURE_BROWSER_XSS_FILTER': getattr(settings, 'SECURE_BROWSER_XSS_FILTER', False),
            'SECURE_CONTENT_TYPE_NOSNIFF': getattr(settings, 'SECURE_CONTENT_TYPE_NOSNIFF', False),
            'X_FRAME_OPTIONS': getattr(settings, 'X_FRAME_OPTIONS', 'DENY'),
        }
        
        print(f"   📋 Configuraciones SSL:")
        for setting, value in ssl_settings.items():
            if isinstance(value, bool):
                status = "✅" if value else "❌"
            elif isinstance(value, int):
                status = "✅" if value > 0 else "❌"
            else:
                status = "✅" if value else "❌"
            
            print(f"      {status} {setting}: {value}")
        
        # Verificar DEBUG
        debug_status = "⚠️" if settings.DEBUG else "✅"
        print(f"   {debug_status} DEBUG: {settings.DEBUG}")
        
        # Verificar ALLOWED_HOSTS
        hosts_status = "✅" if settings.ALLOWED_HOSTS else "⚠️"
        print(f"   {hosts_status} ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error verificando Django: {e}")
        return False

def test_certificate_files():
    """Verificar archivos de certificado local"""
    print(f"\n📁 Verificando archivos de certificado...")
    
    cert_files = [
        'davegames_ssl.crt',
        'davegames_ssl.key',
        'davegames_ssl_advanced.crt',
        'davegames_ssl_advanced.key'
    ]
    
    found_certs = []
    for cert_file in cert_files:
        if os.path.exists(cert_file):
            print(f"   ✅ {cert_file} encontrado")
            found_certs.append(cert_file)
        else:
            print(f"   ❌ {cert_file} no encontrado")
    
    if found_certs:
        print(f"   📋 Para usar certificados locales:")
        print(f"      pip install django-extensions Werkzeug pyOpenSSL")
        print(f"      python manage.py runserver_plus --cert-file {found_certs[0]} --key-file {found_certs[0].replace('.crt', '.key')}")
    
    return len(found_certs) > 0

def main():
    """Función principal"""
    print("🔒 DaveGames - Prueba de Configuración SSL")
    print("=" * 50)
    
    # Verificar argumentos
    if len(sys.argv) > 1:
        url = sys.argv[1]
        if not url.startswith(('http://', 'https://')):
            url = f"https://{url}"
    else:
        url = "https://localhost:8000"
    
    results = []
    
    # Probar configuraciones Django
    results.append(test_django_ssl_settings())
    
    # Verificar archivos de certificado
    results.append(test_certificate_files())
    
    # Probar conexión SSL (solo si no es localhost)
    if 'localhost' not in url and '127.0.0.1' not in url:
        results.append(test_ssl_connection(url))
        results.append(test_http_request(url))
    else:
        print(f"\n⚠️  Saltando pruebas de conexión para localhost")
        print(f"   Para probar SSL local, ejecutar:")
        print(f"   python generate_ssl_cert.py")
        print(f"   python manage.py runserver_plus --cert-file davegames_ssl.crt --key-file davegames_ssl.key")
    
    # Resumen
    print(f"\n" + "=" * 50)
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"🎉 ¡Todas las pruebas pasaron! ({passed}/{total})")
    else:
        print(f"⚠️  Algunas pruebas fallaron ({passed}/{total})")
        print(f"   Revisar configuraciones SSL")
    
    print(f"\n📚 Recursos útiles:")
    print(f"   - SSL Labs: https://www.ssllabs.com/ssltest/")
    print(f"   - Security Headers: https://securityheaders.com/")
    print(f"   - Mozilla Observatory: https://observatory.mozilla.org/")

if __name__ == "__main__":
    main()