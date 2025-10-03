# 🚀 Cómo Subir DaveGames a Vercel

## Paso 1: Instalar Node.js y Vercel CLI

### Opción A: Descargar Node.js

1. Ve a https://nodejs.org/
2. Descarga la versión LTS
3. Instala Node.js

### Opción B: Usar Chocolatey (Windows)

```powershell
# Instalar Chocolatey si no lo tienes
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Instalar Node.js
choco install nodejs
```

### Instalar Vercel CLI

```bash
npm install -g vercel
```

## Paso 2: Preparar el Proyecto

Tu proyecto ya está listo con estos archivos:

- ✅ `vercel.json` - Configuración de Vercel
- ✅ `build_files.sh` - Script de construcción
- ✅ `requirements.txt` - Dependencias actualizadas
- ✅ Settings configurados para producción

## Paso 3: Subir a GitHub (Recomendado)

### Crear repositorio en GitHub:

1. Ve a https://github.com/new
2. Nombre: `davegames`
3. Descripción: `Portal de juegos con Django`
4. Público o Privado (tu elección)
5. Crear repositorio

### Subir código:

```bash
# En la carpeta davegames
git init
git add .
git commit -m "Initial commit - DaveGames project"
git branch -M main
git remote add origin https://github.com/TU-USUARIO/davegames.git
git push -u origin main
```

## Paso 4: Desplegar en Vercel

### Opción A: Desde GitHub (Recomendado)

1. Ve a https://vercel.com/
2. Inicia sesión con GitHub
3. Click "New Project"
4. Importar tu repositorio `davegames`
5. Configurar:
   - Framework Preset: `Other`
   - Build Command: `bash build_files.sh`
   - Output Directory: `staticfiles`
6. Click "Deploy"

### Opción B: Desde CLI

```bash
# En la carpeta davegames
vercel

# Seguir las instrucciones:
# - Set up and deploy? Y
# - Which scope? (tu cuenta)
# - Link to existing project? N
# - Project name: davegames
# - Directory: ./
# - Override settings? N
```

## Paso 5: Configurar Variables de Entorno

En el dashboard de Vercel:

1. Ve a tu proyecto
2. Settings → Environment Variables
3. Agregar:

```
SECRET_KEY = django-insecure-CAMBIA-ESTA-CLAVE-POR-UNA-MUY-LARGA-Y-SEGURA-DE-50-CARACTERES
DEBUG = False
ALLOWED_HOSTS = tu-proyecto.vercel.app
```

## Paso 6: Configurar Base de Datos

### Opción A: Vercel Postgres (Recomendado)

1. En tu proyecto Vercel → Storage
2. Create Database → Postgres
3. Copiar la DATABASE_URL
4. Agregar a Environment Variables:
   ```
   DATABASE_URL = postgresql://username:password@host:port/database
   ```

### Opción B: Usar base de datos externa

- Neon.tech (gratis)
- Supabase (gratis)
- ElephantSQL (gratis)

## Paso 7: Ejecutar Migraciones

Una vez desplegado:

1. Ve a Functions en tu dashboard Vercel
2. O usa Vercel CLI:

```bash
vercel env pull .env.local
python manage.py migrate
```

## Paso 8: Crear Superusuario

```bash
# Localmente con la base de datos de producción
python manage.py createsuperuser
```

## 🎉 ¡Listo!

Tu DaveGames estará disponible en:

- https://tu-proyecto.vercel.app
- Panel admin: https://tu-proyecto.vercel.app/admin

## 🔧 Comandos Útiles

```bash
# Ver logs
vercel logs

# Redesplegar
vercel --prod

# Ver información del proyecto
vercel inspect

# Configurar dominio personalizado
vercel domains add tu-dominio.com
```

## 🚨 Solución de Problemas

### Error: "Application Error"

- Revisar logs: `vercel logs`
- Verificar variables de entorno
- Verificar que build_files.sh sea ejecutable

### Error: "Static files not found"

- Verificar que collectstatic funcione localmente
- Verificar configuración de WhiteNoise

### Error: "Database connection failed"

- Verificar DATABASE_URL
- Verificar que la base de datos esté creada
- Ejecutar migraciones

¡Tu DaveGames estará online en minutos! 🎮✨
