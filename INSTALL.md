# 🎮 DaveGames - Guía de Instalación

## Requisitos del Sistema

- Python 3.8 o superior
- PostgreSQL 12 o superior
- Git (opcional)

## Instalación Paso a Paso

### 1. Clonar o Descargar el Proyecto
```bash
# Si usas Git
git clone <url-del-repositorio>
cd davegames

# O simplemente descarga y extrae el proyecto
```

### 2. Crear Entorno Virtual
```bash
# Crear entorno virtual
python -m venv env

# Activar entorno virtual
# En Windows:
env\Scripts\activate
# En Linux/Mac:
source env/bin/activate
```

### 3. Instalar Dependencias
```bash
# Instalar todas las dependencias
pip install -r requirements.txt

# O instalar manualmente:
pip install Django==4.2.23
pip install psycopg2-binary==2.9.9
pip install Pillow==10.4.0
```

### 4. Configurar PostgreSQL

#### Instalar PostgreSQL
- Descargar desde: https://www.postgresql.org/download/
- Instalar pgAdmin (incluido en la instalación)

#### Crear Base de Datos
```sql
-- Conectarse a PostgreSQL como superusuario
CREATE DATABASE davegames_db;
CREATE USER postgres WITH PASSWORD 'sa654321';
GRANT ALL PRIVILEGES ON DATABASE davegames_db TO postgres;
```

### 5. Configurar Django

#### Variables de Entorno (Opcional)
Crear archivo `.env` en la raíz del proyecto:
```env
DEBUG=True
SECRET_KEY=django-insecure-0a_3q1v324_w-_&=3e)*(+naru#+uk+1w9t++=6$m*+_k17fzi
DB_NAME=davegames_db
DB_USER=postgres
DB_PASSWORD=sa654321
DB_HOST=localhost
DB_PORT=5432
```

#### Aplicar Migraciones
```bash
# Verificar configuración
python manage.py check

# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate
```

#### Crear Superusuario
```bash
python manage.py createsuperuser
```

### 6. Ejecutar el Servidor
```bash
python manage.py runserver
```

## Acceso a la Aplicación

- **Frontend**: http://127.0.0.1:8000/
- **Panel Admin**: http://127.0.0.1:8000/admin/

## Estructura del Proyecto

```
davegames/
├── davegames_project/          # Configuración principal
│   ├── settings.py            # Configuraciones
│   ├── urls.py               # URLs principales
│   └── wsgi.py               # WSGI para producción
├── games/                     # App principal
│   ├── models.py             # Modelos de datos
│   ├── views.py              # Vistas
│   ├── admin.py              # Configuración admin
│   ├── urls.py               # URLs de la app
│   └── templates/            # Templates HTML
├── media/                     # Archivos subidos
├── static/                    # Archivos estáticos
├── requirements.txt           # Dependencias
├── manage.py                 # Comando Django
└── check_db.py               # Script de verificación
```

## Características Principales

### 🎯 Funcionalidades
- ✅ Gestión de categorías de juegos
- ✅ Catálogo de juegos con imágenes
- ✅ Panel de administración completo
- ✅ Diseño responsive con tema gamer
- ✅ Base de datos PostgreSQL
- ✅ Sistema de requisitos mínimos/recomendados
- ✅ Enlaces de descarga y trailers

### 🎨 Diseño
- Colores gamers (verde neón, magenta, cyan)
- Animaciones CSS
- Efectos de hover y transiciones
- Tipografías gaming (Orbitron, Rajdhani)
- Responsive design

### 🔧 Tecnologías
- **Backend**: Django 4.2.23
- **Base de Datos**: PostgreSQL
- **Frontend**: HTML5, CSS3, JavaScript
- **Framework CSS**: Bootstrap 5.3
- **Iconos**: Font Awesome 6.4
- **Fuentes**: Google Fonts

## Comandos Útiles

```bash
# Verificar base de datos
python check_db.py

# Crear nueva migración
python manage.py makemigrations games

# Ver SQL de migraciones
python manage.py sqlmigrate games 0001

# Shell de Django
python manage.py shell

# Recopilar archivos estáticos (producción)
python manage.py collectstatic

# Crear datos de prueba
python manage.py loaddata fixtures/sample_data.json
```

## Solución de Problemas

### Error de conexión a PostgreSQL
1. Verificar que PostgreSQL esté ejecutándose
2. Comprobar credenciales en `settings.py`
3. Verificar que la base de datos existe

### Error de psycopg2
```bash
pip uninstall psycopg2-binary
pip install psycopg2-binary==2.9.9
```

### Error de Pillow
```bash
pip install --upgrade Pillow
```

## Contacto y Soporte

Para problemas o sugerencias, contacta al desarrollador.

---
**DaveGames** - Tu portal definitivo para descubrir juegos 🎮