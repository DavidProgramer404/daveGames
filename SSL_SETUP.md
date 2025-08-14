# 🔒 DaveGames - Configuración SSL/HTTPS

## 📋 Opciones para Implementar SSL

### 1. 🏠 Desarrollo Local (Self-Signed Certificate)
### 2. 🌐 Producción con Let's Encrypt (Gratuito)
### 3. ☁️ Despliegue en la Nube (Heroku, DigitalOcean, AWS)
### 4. 🔧 Nginx + Gunicorn con SSL

---

## 1. 🏠 SSL para Desarrollo Local

### Opción A: Django Extensions (Recomendado para desarrollo)

#### Instalar django-extensions
```bash
pip install django-extensions
pip install Werkzeug
pip install pyOpenSSL
```

#### Configurar settings.py
```python
# En INSTALLED_APPS
INSTALLED_APPS = [
    # ... otras apps
    'django_extensions',
]

# Configuración SSL para desarrollo
if DEBUG:
    SECURE_SSL_REDIRECT = False
else:
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
```

#### Ejecutar servidor con SSL
```bash
python manage.py runserver_plus --cert-file cert.crt --key-file cert.key
```

### Opción B: Certificado Self-Signed Manual

#### Generar certificado
```bash
# Instalar OpenSSL (Windows: descargar desde openssl.org)
# Generar clave privada
openssl genrsa -out server.key 2048

# Generar certificado
openssl req -new -x509 -key server.key -out server.crt -days 365

# Información requerida:
# Country Name: ES
# State: Tu Estado
# City: Tu Ciudad  
# Organization: DaveGames
# Organizational Unit: IT Department
# Common Name: localhost (IMPORTANTE)
# Email: admin@davegames.com
```

#### Ejecutar con certificado
```bash
python manage.py runsslserver --certificate server.crt --key server.key
```

---

## 2. 🌐 Producción con Let's Encrypt (GRATUITO)

### Configuración con Nginx + Gunicorn

#### Instalar Certbot
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install certbot python3-certbot-nginx

# CentOS/RHEL
sudo yum install certbot python3-certbot-nginx
```

#### Configurar Nginx
```nginx
# /etc/nginx/sites-available/davegames
server {
    listen 80;
    server_name tu-dominio.com www.tu-dominio.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location /static/ {
        alias /path/to/davegames/staticfiles/;
    }
    
    location /media/ {
        alias /path/to/davegames/media/;
    }
}
```

#### Obtener certificado SSL
```bash
# Obtener certificado automáticamente
sudo certbot --nginx -d tu-dominio.com -d www.tu-dominio.com

# Renovación automática
sudo crontab -e
# Agregar línea:
0 12 * * * /usr/bin/certbot renew --quiet
```

---

## 3. ☁️ Despliegue en la Nube

### Heroku (SSL Automático)
```bash
# Instalar Heroku CLI
# Crear Procfile
echo "web: gunicorn davegames_project.wsgi" > Procfile

# Configurar requirements.txt
echo "gunicorn" >> requirements.txt
echo "whitenoise" >> requirements.txt

# Deploy
heroku create tu-app-davegames
git push heroku main

# SSL automático en Heroku (gratis para dominios .herokuapp.com)
```

### DigitalOcean App Platform
```yaml
# .do/app.yaml
name: davegames
services:
- name: web
  source_dir: /
  github:
    repo: tu-usuario/davegames
    branch: main
  run_command: gunicorn --worker-tmp-dir /dev/shm davegames_project.wsgi
  environment_slug: python
  instance_count: 1
  instance_size_slug: basic-xxs
  routes:
  - path: /
  envs:
  - key: DEBUG
    value: "False"
```

---

## 4. 🔧 Configuración Django para SSL

### Actualizar settings.py para Producción
```python
# davegames_project/settings.py

import os
from decouple import config

# SSL/HTTPS Settings
if not DEBUG:
    # Forzar HTTPS
    SECURE_SSL_REDIRECT = True
    
    # Configuración de seguridad HTTPS
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_HSTS_SECONDS = 31536000  # 1 año
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    
    # Cookies seguras
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    
    # Configuración adicional de seguridad
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    
    # Hosts permitidos
    ALLOWED_HOSTS = [
        'tu-dominio.com',
        'www.tu-dominio.com',
        'localhost',
        '127.0.0.1',
    ]

# Configuración de archivos estáticos para producción
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Middleware para WhiteNoise (servir archivos estáticos)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Agregar esto
    # ... resto del middleware
]
```

---

## 5. 🐳 Docker con SSL

### Dockerfile
```dockerfile
FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "davegames_project.wsgi:application"]
```

### docker-compose.yml con Nginx y SSL
```yaml
version: '3.8'

services:
  web:
    build: .
    volumes:
      - .:/app
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    expose:
      - 8000
    environment:
      - DEBUG=False
    depends_on:
      - db

  db:
    image: postgres:13
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    environment:
      - POSTGRES_DB=davegames_db
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=sa654321

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    depends_on:
      - web

volumes:
  postgres_data:
  static_volume:
  media_volume:
```

---

## 6. 📋 Checklist de Seguridad SSL

### ✅ Configuraciones Obligatorias
- [ ] `SECURE_SSL_REDIRECT = True`
- [ ] `SESSION_COOKIE_SECURE = True`
- [ ] `CSRF_COOKIE_SECURE = True`
- [ ] `SECURE_HSTS_SECONDS` configurado
- [ ] `ALLOWED_HOSTS` actualizado
- [ ] Certificado SSL válido instalado

### ✅ Configuraciones Recomendadas
- [ ] `SECURE_HSTS_INCLUDE_SUBDOMAINS = True`
- [ ] `SECURE_HSTS_PRELOAD = True`
- [ ] `SECURE_BROWSER_XSS_FILTER = True`
- [ ] `SECURE_CONTENT_TYPE_NOSNIFF = True`
- [ ] `X_FRAME_OPTIONS = 'DENY'`

### ✅ Pruebas
- [ ] Verificar redirección HTTP → HTTPS
- [ ] Probar certificado en navegador
- [ ] Verificar headers de seguridad
- [ ] Probar en SSL Labs: https://www.ssllabs.com/ssltest/

---

## 7. 🛠️ Scripts de Automatización

### Script para desarrollo local con SSL
```bash
#!/bin/bash
# ssl_dev.sh

echo "🔒 Configurando SSL para desarrollo..."

# Instalar dependencias
pip install django-extensions Werkzeug pyOpenSSL

# Generar certificado si no existe
if [ ! -f "cert.crt" ]; then
    echo "📜 Generando certificado self-signed..."
    openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.crt -days 365 -nodes \
        -subj "/C=ES/ST=Madrid/L=Madrid/O=DaveGames/CN=localhost"
fi

# Ejecutar servidor SSL
echo "🚀 Iniciando servidor HTTPS en https://localhost:8000"
python manage.py runserver_plus --cert-file cert.crt --key-file key.pem
```

### Script para producción
```bash
#!/bin/bash
# ssl_prod.sh

echo "🌐 Configurando SSL para producción..."

# Instalar Certbot
sudo apt update
sudo apt install certbot python3-certbot-nginx -y

# Obtener certificado
sudo certbot --nginx -d $1 -d www.$1 --non-interactive --agree-tos --email admin@$1

# Configurar renovación automática
(crontab -l 2>/dev/null; echo "0 12 * * * /usr/bin/certbot renew --quiet") | crontab -

echo "✅ SSL configurado para $1"
```

---

## 8. 🔍 Verificación y Monitoreo

### Comandos de verificación
```bash
# Verificar certificado
openssl x509 -in cert.crt -text -noout

# Probar conexión SSL
openssl s_client -connect tu-dominio.com:443

# Verificar headers de seguridad
curl -I https://tu-dominio.com

# Verificar redirección
curl -I http://tu-dominio.com
```

### Herramientas online
- **SSL Labs**: https://www.ssllabs.com/ssltest/
- **Security Headers**: https://securityheaders.com/
- **Mozilla Observatory**: https://observatory.mozilla.org/

---

## 9. 💰 Costos y Opciones

| Opción | Costo | Dificultad | Recomendado para |
|--------|-------|------------|------------------|
| Self-Signed | Gratis | Fácil | Desarrollo |
| Let's Encrypt | Gratis | Medio | Producción |
| Cloudflare | Gratis/Pago | Fácil | Cualquier entorno |
| Heroku SSL | Gratis | Muy fácil | Despliegue rápido |
| AWS Certificate Manager | Gratis | Medio | AWS |

---

## 🚨 Problemas Comunes

### Error: "Mixed Content"
```python
# En settings.py
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
```

### Error: "Certificate not trusted"
- Usar certificado de CA válida (Let's Encrypt)
- Para desarrollo: aceptar certificado en navegador

### Error: "Redirect loop"
```python
# Verificar configuración del proxy
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
```

---

## 📞 Soporte

Para problemas específicos con SSL en DaveGames:
1. Revisar logs de Django y servidor web
2. Verificar configuración de DNS
3. Probar con herramientas online
4. Consultar documentación de tu proveedor de hosting

---

**🔒 ¡Tu DaveGames estará seguro con HTTPS! 🔒**