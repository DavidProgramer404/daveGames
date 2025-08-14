# 🚀 DaveGames - Guía de Despliegue

## 📋 Opciones de Despliegue

### 1. 🟢 Vercel (Recomendado para Django)
### 2. 🔵 Netlify (Solo frontend estático)
### 3. 🟣 Heroku (Clásico para Django)
### 4. 🟠 Railway (Alternativa moderna)

---

## 🟢 Despliegue en Vercel

### Preparación
```bash
# 1. Instalar Vercel CLI
npm i -g vercel

# 2. Instalar dependencias adicionales
pip install dj-database-url whitenoise python-decouple

# 3. Actualizar requirements.txt
cp requirements_vercel.txt requirements.txt
```

### Configuración
```bash
# 1. Inicializar proyecto Vercel
vercel

# 2. Configurar variables de entorno en Vercel Dashboard
# - SECRET_KEY: tu-clave-secreta-django
# - DATABASE_URL: postgresql://user:pass@host:port/db
# - DEBUG: False
```

### Variables de Entorno Vercel
```env
SECRET_KEY=tu-clave-secreta-muy-larga-y-segura
DATABASE_URL=postgresql://username:password@hostname:port/database
DEBUG=False
DJANGO_SETTINGS_MODULE=vercel_settings
```

### Comandos de Despliegue
```bash
# Desplegar
vercel --prod

# Ver logs
vercel logs

# Configurar dominio personalizado
vercel domains add tu-dominio.com
```

### Estructura para Vercel
```
davegames/
├── vercel.json              # Configuración Vercel
├── build_files.sh          # Script de construcción
├── vercel_settings.py      # Settings para Vercel
├── requirements_vercel.txt # Dependencias optimizadas
└── davegames_project/
    └── wsgi.py            # Punto de entrada
```

---

## 🔵 Despliegue en Netlify

⚠️ **Nota**: Netlify no soporta Django directamente. Opciones:

### Opción A: Frontend Estático + API Externa
```bash
# 1. Generar sitio estático desde Django
python manage.py collectstatic
python manage.py generate_static_site  # Custom command

# 2. Subir solo el frontend a Netlify
# 3. Usar API Django en Heroku/Vercel
```

### Opción B: Netlify Functions (Limitado)
```bash
# Solo para funciones simples, no recomendado para Django completo
```

### Configuración Netlify
```toml
# netlify.toml
[build]
  publish = "staticfiles"
  command = "python manage.py collectstatic --noinput"

[[redirects]]
  from = "/api/*"
  to = "https://tu-api-django.herokuapp.com/api/:splat"
  status = 200
```

---

## 🟣 Despliegue en Heroku

### Preparación
```bash
# 1. Instalar Heroku CLI
# 2. Crear archivos necesarios
echo "web: gunicorn davegames_project.wsgi" > Procfile
echo "python-3.9.18" > runtime.txt
```

### Configuración
```bash
# 1. Crear app Heroku
heroku create davegames-app

# 2. Configurar variables
heroku config:set SECRET_KEY=tu-clave-secreta
heroku config:set DEBUG=False
heroku config:set DJANGO_SETTINGS_MODULE=davegames_project.settings

# 3. Agregar PostgreSQL
heroku addons:create heroku-postgresql:mini

# 4. Desplegar
git push heroku main

# 5. Migrar base de datos
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

---

## 🟠 Despliegue en Railway

### Preparación
```bash
# 1. Instalar Railway CLI
npm install -g @railway/cli

# 2. Login
railway login
```

### Configuración
```bash
# 1. Inicializar proyecto
railway init

# 2. Agregar PostgreSQL
railway add postgresql

# 3. Configurar variables
railway variables set SECRET_KEY=tu-clave-secreta
railway variables set DEBUG=False

# 4. Desplegar
railway up
```

---

## 📊 Comparación de Plataformas

| Plataforma | Django | PostgreSQL | SSL | Precio | Facilidad |
|------------|--------|------------|-----|--------|-----------|
| **Vercel** | ✅ | ✅ | ✅ | Gratis/Pago | ⭐⭐⭐⭐ |
| **Heroku** | ✅ | ✅ | ✅ | Pago | ⭐⭐⭐⭐⭐ |
| **Railway** | ✅ | ✅ | ✅ | Gratis/Pago | ⭐⭐⭐⭐ |
| **Netlify** | ❌ | ❌ | ✅ | Gratis | ⭐⭐ |

---

## 🔧 Configuraciones Específicas

### Para Vercel
```python
# vercel_settings.py
ALLOWED_HOSTS = ['.vercel.app', 'tu-dominio.com']
DATABASES = {'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))}
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

### Para Heroku
```python
# settings.py
import dj_database_url
DATABASES['default'] = dj_database_url.config(conn_max_age=600)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
```

### Para Railway
```python
# settings.py
ALLOWED_HOSTS = ['.railway.app', 'tu-dominio.com']
DATABASES = {'default': dj_database_url.config()}
```

---

## 🚀 Pasos de Despliegue Recomendados

### 1. Preparar Proyecto
```bash
# Instalar dependencias de producción
pip install gunicorn whitenoise dj-database-url python-decouple

# Actualizar requirements.txt
pip freeze > requirements.txt

# Configurar archivos estáticos
python manage.py collectstatic
```

### 2. Configurar Variables de Entorno
```env
SECRET_KEY=clave-super-secreta-de-50-caracteres-minimo
DEBUG=False
DATABASE_URL=postgresql://user:pass@host:port/db
ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com
```

### 3. Probar Localmente
```bash
# Simular producción
export DEBUG=False
export SECRET_KEY=test-key
python manage.py runserver
```

### 4. Desplegar
```bash
# Vercel
vercel --prod

# Heroku
git push heroku main

# Railway
railway up
```

### 5. Post-Despliegue
```bash
# Migrar base de datos
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Verificar SSL
python test_ssl.py https://tu-dominio.com
```

---

## 🔍 Verificación Post-Despliegue

### Checklist
- [ ] ✅ Sitio carga correctamente
- [ ] ✅ SSL/HTTPS funcionando
- [ ] ✅ Base de datos conectada
- [ ] ✅ Archivos estáticos servidos
- [ ] ✅ Panel admin accesible
- [ ] ✅ Formularios funcionando
- [ ] ✅ Imágenes subiendo correctamente

### Herramientas de Verificación
```bash
# Probar SSL
python test_ssl.py https://tu-dominio.com

# Verificar headers de seguridad
curl -I https://tu-dominio.com

# Probar velocidad
https://pagespeed.web.dev/
```

---

## 🆘 Solución de Problemas

### Error: "Application Error"
```bash
# Ver logs
vercel logs  # Vercel
heroku logs --tail  # Heroku
railway logs  # Railway
```

### Error: "Static files not found"
```python
# Verificar configuración
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

### Error: "Database connection failed"
```bash
# Verificar DATABASE_URL
echo $DATABASE_URL
python manage.py dbshell
```

---

## 📞 Soporte

Para problemas específicos:
1. Revisar logs de la plataforma
2. Verificar variables de entorno
3. Probar configuración localmente
4. Consultar documentación oficial

---

**🎮 ¡Tu DaveGames estará online en minutos! 🚀**