# 🎮 DaveGames - Portal de Juegos

![DaveGames](https://img.shields.io/badge/DaveGames-Portal%20de%20Juegos-00ff88?style=for-the-badge&logo=gamepad)
![Django](https://img.shields.io/badge/Django-4.2.23-092E20?style=for-the-badge&logo=django)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17.5-316192?style=for-the-badge&logo=postgresql)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python)

## 📋 Descripción

**DaveGames** es un portal web moderno para la gestión y descarga de juegos, desarrollado con Django y PostgreSQL. Cuenta con un diseño profesional con temática gamer, panel de administración completo y funcionalidades avanzadas para catalogar juegos por categorías.

## ✨ Características Principales

### 🎯 Funcionalidades
- ✅ **Catálogo de Juegos**: Gestión completa de juegos con imágenes, descripciones y enlaces
- ✅ **Categorías**: Organización por géneros y plataformas
- ✅ **Panel Admin**: Interfaz administrativa completa para gestionar contenido
- ✅ **Requisitos del Sistema**: Especificaciones mínimas y recomendadas
- ✅ **Multimedia**: Soporte para imágenes de portada y enlaces de trailers
- ✅ **Enlaces de Descarga**: Gestión de enlaces directos de descarga

### 🎨 Diseño
- 🌈 **Tema Gamer**: Colores neón (verde, magenta, cyan) con efectos visuales
- 📱 **Responsive**: Adaptable a dispositivos móviles y desktop
- ⚡ **Animaciones**: Efectos CSS modernos y transiciones suaves
- 🎭 **Tipografías Gaming**: Fuentes Orbitron y Rajdhani
- 🎪 **Efectos Visuales**: Gradientes, sombras neón y animaciones de fondo

### 🔧 Tecnologías
- **Backend**: Django 4.2.23
- **Base de Datos**: PostgreSQL 17.5
- **Frontend**: HTML5, CSS3, JavaScript ES6
- **Framework CSS**: Bootstrap 5.3
- **Iconos**: Font Awesome 6.4
- **Fuentes**: Google Fonts

## 🚀 Instalación Rápida

### Prerrequisitos
- Python 3.8+
- PostgreSQL 12+
- Git (opcional)

### 1. Clonar el Proyecto
```bash
git clone <url-del-repositorio>
cd davegames
```

### 2. Configurar Entorno Virtual
```bash
# Crear entorno virtual
python -m venv env

# Activar entorno virtual
# Windows:
env\Scripts\activate
# Linux/Mac:
source env/bin/activate
```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar Base de Datos
```sql
-- En PostgreSQL
CREATE DATABASE davegames_db;
```

### 5. Configurar Django
```bash
# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Verificar instalación
python verify_installation.py
```

### 6. Ejecutar Servidor
```bash
python manage.py runserver
```

## 🌐 Acceso

- **Frontend**: http://127.0.0.1:8000/
- **Panel Admin**: http://127.0.0.1:8000/admin/

## 📁 Estructura del Proyecto

```
davegames/
├── 📁 davegames_project/      # Configuración principal
│   ├── ⚙️ settings.py        # Configuraciones Django
│   ├── 🔗 urls.py            # URLs principales
│   └── 🚀 wsgi.py            # WSGI para producción
├── 📁 games/                  # Aplicación principal
│   ├── 📊 models.py          # Modelos de datos
│   ├── 👁️ views.py           # Vistas y lógica
│   ├── 🔧 admin.py           # Panel de administración
│   ├── 🔗 urls.py            # URLs de la app
│   └── 📁 templates/         # Templates HTML
│       └── 📁 games/
│           ├── 🏠 base.html
│           ├── 🏡 home.html
│           ├── 📂 category_games.html
│           └── 🎮 game_detail.html
├── 📁 media/                  # Archivos subidos
├── 📁 static/                 # Archivos estáticos
├── 📋 requirements.txt        # Dependencias Python
├── 🔍 verify_installation.py  # Script de verificación
├── 🔍 check_db.py            # Verificación de BD
├── ⚙️ manage.py              # Comando Django
├── 📖 README.md              # Este archivo
├── 📋 INSTALL.md             # Guía de instalación
└── 🚫 .gitignore             # Archivos ignorados
```

## 📊 Modelos de Datos

### Category (Categoría)
```python
- name: CharField(100)           # Nombre de la categoría
- description: TextField         # Descripción opcional
```

### Game (Juego)
```python
- title: CharField(200)          # Título del juego
- category: ForeignKey           # Categoría del juego
- description: TextField         # Descripción completa
- min_requirements: TextField    # Requisitos mínimos
- max_requirements: TextField    # Requisitos recomendados
- cover_image: ImageField        # Imagen de portada
- trailer_url: URLField          # Enlace del trailer
- download_link: URLField        # Enlace de descarga
- release_date: DateField        # Fecha de lanzamiento
```

## 🎨 Paleta de Colores

```css
--primary-color: #00ff88      /* Verde neón */
--secondary-color: #ff0080    /* Magenta */
--accent-color: #00d4ff       /* Cyan */
--dark-bg: #0a0a0a           /* Fondo oscuro */
--card-bg: #1a1a1a           /* Fondo de tarjetas */
```

## 📱 Capturas de Pantalla

### 🏠 Página Principal
- Hero section con animaciones
- Estadísticas del sitio
- Juegos destacados
- Categorías disponibles

### 🎮 Detalle del Juego
- Información completa del juego
- Requisitos del sistema
- Enlaces de descarga y trailer
- Botones de compartir

### 🔧 Panel de Administración
- Gestión de categorías
- Gestión de juegos
- Interfaz personalizada

## 🛠️ Comandos Útiles

```bash
# Verificar instalación
python verify_installation.py

# Verificar base de datos
python check_db.py

# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Ejecutar servidor
python manage.py runserver

# Shell de Django
python manage.py shell

# Recopilar archivos estáticos
python manage.py collectstatic
```

## 🔧 Configuración de Producción

### Variables de Entorno
Crear archivo `.env`:
```env
DEBUG=False
SECRET_KEY=tu-clave-secreta-aqui
DB_NAME=davegames_db
DB_USER=postgres
DB_PASSWORD=tu-password
DB_HOST=localhost
DB_PORT=5432
ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com
```

### Dependencias Adicionales para Producción
```bash
pip install gunicorn whitenoise python-decouple
```

## 🔒 Configuración SSL/HTTPS

### Desarrollo Local
```bash
# Generar certificado SSL
python generate_ssl_cert.py

# Instalar dependencias SSL
pip install django-extensions Werkzeug pyOpenSSL

# Ejecutar servidor con SSL
python manage.py runserver_plus --cert-file davegames_ssl.crt --key-file davegames_ssl.key
```

### Producción con Let's Encrypt
```bash
# Configuración automática (Ubuntu/Debian)
sudo chmod +x setup_production_ssl.sh
sudo ./setup_production_ssl.sh tu-dominio.com admin@tu-dominio.com
```

### Verificar SSL
```bash
# Probar configuraciones SSL
python test_ssl.py

# Probar sitio específico
python test_ssl.py https://tu-dominio.com
```

### Proveedores de Hosting
- **Heroku**: SSL automático incluido
- **DigitalOcean**: App Platform con SSL automático
- **AWS**: Certificate Manager gratuito
- **Cloudflare**: SSL gratuito con proxy

Ver `SSL_SETUP.md` para guía completa de configuración SSL.

## 🐛 Solución de Problemas

### Error de PostgreSQL
```bash
# Reinstalar driver
pip uninstall psycopg2-binary
pip install psycopg2-binary==2.9.9
```

### Error de Pillow
```bash
pip install --upgrade Pillow
```

### Error de Migraciones
```bash
python manage.py makemigrations --empty games
python manage.py migrate --fake-initial
```

## 🚀 Despliegue en la Nube

### Vercel (Recomendado)
```bash
# Configurar proyecto
python deploy_vercel.py

# O manualmente
npm i -g vercel
vercel
```

### Heroku
```bash
# Crear app
heroku create davegames-app
git push heroku main
heroku run python manage.py migrate
```

### Railway
```bash
# Desplegar
railway login
railway init
railway up
```

### Netlify (Solo frontend)
```bash
# Para sitios estáticos únicamente
python manage.py collectstatic
# Subir carpeta staticfiles/
```

Ver `DEPLOYMENT_GUIDE.md` para guías detalladas de cada plataforma.

## 📈 Roadmap

- [ ] Sistema de usuarios y autenticación
- [ ] Comentarios y valoraciones
- [ ] API REST
- [ ] Búsqueda avanzada
- [ ] Sistema de favoritos
- [ ] Notificaciones
- [ ] Integración con redes sociales

## 🤝 Contribuir

1. Fork el proyecto
2. Crear rama feature (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 👨‍💻 Autor

**Dave** - Desarrollador Principal

## 🙏 Agradecimientos

- Django Community
- Bootstrap Team
- Font Awesome
- Google Fonts
- PostgreSQL Team

---

<div align="center">

**🎮 DaveGames - Tu portal definitivo para descubrir juegos 🎮**

[![Made with ❤️](https://img.shields.io/badge/Made%20with-❤️-red.svg)](https://github.com/tu-usuario/davegames)
[![Django](https://img.shields.io/badge/Powered%20by-Django-092E20.svg)](https://djangoproject.com/)

</div>