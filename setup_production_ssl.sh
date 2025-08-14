#!/bin/bash

# DaveGames - Script de configuración SSL para producción
# Configuración automática de SSL con Let's Encrypt y Nginx

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para imprimir mensajes
print_message() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}🎮 DaveGames - Configuración SSL Producción${NC}"
    echo "=================================================="
}

# Verificar si se ejecuta como root
check_root() {
    if [[ $EUID -ne 0 ]]; then
        print_error "Este script debe ejecutarse como root (sudo)"
        exit 1
    fi
}

# Verificar argumentos
check_arguments() {
    if [ $# -eq 0 ]; then
        print_error "Uso: $0 <dominio> [email]"
        print_error "Ejemplo: $0 davegames.com admin@davegames.com"
        exit 1
    fi
    
    DOMAIN=$1
    EMAIL=${2:-"admin@$DOMAIN"}
    
    print_message "Dominio: $DOMAIN"
    print_message "Email: $EMAIL"
}

# Instalar dependencias
install_dependencies() {
    print_message "Instalando dependencias..."
    
    # Actualizar sistema
    apt update
    
    # Instalar Nginx si no está instalado
    if ! command -v nginx &> /dev/null; then
        print_message "Instalando Nginx..."
        apt install -y nginx
    fi
    
    # Instalar Certbot
    if ! command -v certbot &> /dev/null; then
        print_message "Instalando Certbot..."
        apt install -y certbot python3-certbot-nginx
    fi
    
    # Instalar Python y dependencias
    apt install -y python3-pip python3-venv
    
    print_message "✅ Dependencias instaladas"
}

# Configurar Nginx
configure_nginx() {
    print_message "Configurando Nginx..."
    
    # Crear configuración de Nginx
    cat > /etc/nginx/sites-available/davegames << EOF
server {
    listen 80;
    server_name $DOMAIN www.$DOMAIN;
    
    # Redirigir a HTTPS (se configurará después)
    return 301 https://\$server_name\$request_uri;
}

server {
    listen 443 ssl http2;
    server_name $DOMAIN www.$DOMAIN;
    
    # Configuración SSL (se completará con Certbot)
    
    # Configuración de seguridad
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
    
    # Configuración de archivos estáticos
    location /static/ {
        alias /var/www/davegames/staticfiles/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    location /media/ {
        alias /var/www/davegames/media/;
        expires 1y;
        add_header Cache-Control "public";
    }
    
    # Proxy a Django
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_set_header X-Forwarded-Host \$server_name;
        proxy_redirect off;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
    
    # Configuración para archivos grandes
    client_max_body_size 100M;
}
EOF
    
    # Habilitar sitio
    ln -sf /etc/nginx/sites-available/davegames /etc/nginx/sites-enabled/
    
    # Remover configuración por defecto
    rm -f /etc/nginx/sites-enabled/default
    
    # Verificar configuración
    nginx -t
    
    print_message "✅ Nginx configurado"
}

# Obtener certificado SSL
obtain_ssl_certificate() {
    print_message "Obteniendo certificado SSL..."
    
    # Reiniciar Nginx
    systemctl restart nginx
    
    # Obtener certificado
    certbot --nginx -d $DOMAIN -d www.$DOMAIN \
        --non-interactive \
        --agree-tos \
        --email $EMAIL \
        --redirect
    
    print_message "✅ Certificado SSL obtenido"
}

# Configurar renovación automática
setup_auto_renewal() {
    print_message "Configurando renovación automática..."
    
    # Crear script de renovación
    cat > /etc/cron.d/certbot-renew << EOF
# Renovar certificados SSL automáticamente
0 12 * * * root /usr/bin/certbot renew --quiet --post-hook "systemctl reload nginx"
EOF
    
    # Probar renovación
    certbot renew --dry-run
    
    print_message "✅ Renovación automática configurada"
}

# Configurar firewall
configure_firewall() {
    print_message "Configurando firewall..."
    
    if command -v ufw &> /dev/null; then
        ufw allow 'Nginx Full'
        ufw allow ssh
        ufw --force enable
        print_message "✅ Firewall configurado"
    else
        print_warning "UFW no está instalado, configurar firewall manualmente"
    fi
}

# Crear directorio para la aplicación
setup_app_directory() {
    print_message "Configurando directorio de aplicación..."
    
    # Crear directorio
    mkdir -p /var/www/davegames
    
    # Configurar permisos
    chown -R www-data:www-data /var/www/davegames
    chmod -R 755 /var/www/davegames
    
    print_message "✅ Directorio configurado en /var/www/davegames"
}

# Crear servicio systemd para Gunicorn
create_gunicorn_service() {
    print_message "Creando servicio Gunicorn..."
    
    cat > /etc/systemd/system/davegames.service << EOF
[Unit]
Description=DaveGames Django Application
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/davegames
Environment="PATH=/var/www/davegames/venv/bin"
ExecStart=/var/www/davegames/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:8000 davegames_project.wsgi:application
Restart=always

[Install]
WantedBy=multi-user.target
EOF
    
    # Recargar systemd
    systemctl daemon-reload
    
    print_message "✅ Servicio Gunicorn creado"
}

# Mostrar resumen final
show_summary() {
    print_header
    print_message "🎉 ¡Configuración SSL completada!"
    echo ""
    print_message "📋 Resumen:"
    print_message "   - Dominio: $DOMAIN"
    print_message "   - Certificado SSL: ✅ Instalado"
    print_message "   - Nginx: ✅ Configurado"
    print_message "   - Renovación automática: ✅ Configurada"
    print_message "   - Firewall: ✅ Configurado"
    echo ""
    print_message "📁 Próximos pasos:"
    print_message "   1. Subir código de DaveGames a /var/www/davegames"
    print_message "   2. Instalar dependencias Python en venv"
    print_message "   3. Configurar variables de entorno"
    print_message "   4. Ejecutar migraciones Django"
    print_message "   5. Iniciar servicio: systemctl start davegames"
    echo ""
    print_message "🌐 Tu sitio estará disponible en: https://$DOMAIN"
    echo ""
    print_message "🔍 Verificar SSL en: https://www.ssllabs.com/ssltest/analyze.html?d=$DOMAIN"
}

# Función principal
main() {
    print_header
    
    check_root
    check_arguments "$@"
    
    print_message "Iniciando configuración SSL para $DOMAIN..."
    read -p "¿Continuar? (y/N): " -n 1 -r
    echo
    
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_error "Configuración cancelada"
        exit 1
    fi
    
    install_dependencies
    configure_nginx
    obtain_ssl_certificate
    setup_auto_renewal
    configure_firewall
    setup_app_directory
    create_gunicorn_service
    
    show_summary
}

# Ejecutar función principal
main "$@"