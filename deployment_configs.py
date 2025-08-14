"""
Configuraciones de despliegue para diferentes proveedores
DaveGames - Portal de Juegos
"""

import os

# ============================================================================
# HEROKU CONFIGURATION
# ============================================================================

HEROKU_SETTINGS = {
    'ALLOWED_HOSTS': ['.herokuapp.com'],
    'SECURE_SSL_REDIRECT': True,
    'SECURE_PROXY_SSL_HEADER': ('HTTP_X_FORWARDED_PROTO', 'https'),
    'SESSION_COOKIE_SECURE': True,
    'CSRF_COOKIE_SECURE': True,
    'SECURE_HSTS_SECONDS': 31536000,
    'SECURE_HSTS_INCLUDE_SUBDOMAINS': True,
    'SECURE_HSTS_PRELOAD': True,
    'SECURE_BROWSER_XSS_FILTER': True,
    'SECURE_CONTENT_TYPE_NOSNIFF': True,
    'X_FRAME_OPTIONS': 'DENY',
    
    # Database
    'DATABASES': {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('DATABASE_URL'),
        }
    },
    
    # Static files
    'STATICFILES_STORAGE': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
    'STATIC_ROOT': os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'staticfiles'),
    
    # Middleware
    'MIDDLEWARE_ADDITIONS': [
        'whitenoise.middleware.WhiteNoiseMiddleware',
    ]
}

# ============================================================================
# DIGITALOCEAN APP PLATFORM
# ============================================================================

DIGITALOCEAN_SETTINGS = {
    'ALLOWED_HOSTS': ['.ondigitalocean.app', '.your-domain.com'],
    'SECURE_SSL_REDIRECT': True,
    'SECURE_PROXY_SSL_HEADER': ('HTTP_X_FORWARDED_PROTO', 'https'),
    'SESSION_COOKIE_SECURE': True,
    'CSRF_COOKIE_SECURE': True,
    'SECURE_HSTS_SECONDS': 31536000,
    'SECURE_HSTS_INCLUDE_SUBDOMAINS': True,
    'SECURE_HSTS_PRELOAD': True,
    
    # Database
    'DATABASES': {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('DB_NAME'),
            'USER': os.environ.get('DB_USER'),
            'PASSWORD': os.environ.get('DB_PASSWORD'),
            'HOST': os.environ.get('DB_HOST'),
            'PORT': os.environ.get('DB_PORT', '5432'),
        }
    }
}

# ============================================================================
# AWS ELASTIC BEANSTALK
# ============================================================================

AWS_SETTINGS = {
    'ALLOWED_HOSTS': ['.elasticbeanstalk.com', '.your-domain.com'],
    'SECURE_SSL_REDIRECT': True,
    'SECURE_PROXY_SSL_HEADER': ('HTTP_X_FORWARDED_PROTO', 'https'),
    'SESSION_COOKIE_SECURE': True,
    'CSRF_COOKIE_SECURE': True,
    'SECURE_HSTS_SECONDS': 31536000,
    'SECURE_HSTS_INCLUDE_SUBDOMAINS': True,
    'SECURE_HSTS_PRELOAD': True,
    
    # AWS specific
    'AWS_ACCESS_KEY_ID': os.environ.get('AWS_ACCESS_KEY_ID'),
    'AWS_SECRET_ACCESS_KEY': os.environ.get('AWS_SECRET_ACCESS_KEY'),
    'AWS_STORAGE_BUCKET_NAME': os.environ.get('AWS_STORAGE_BUCKET_NAME'),
    'AWS_S3_REGION_NAME': os.environ.get('AWS_S3_REGION_NAME', 'us-east-1'),
    
    # Static files en S3
    'DEFAULT_FILE_STORAGE': 'storages.backends.s3boto3.S3Boto3Storage',
    'STATICFILES_STORAGE': 'storages.backends.s3boto3.S3StaticStorage',
    'AWS_S3_CUSTOM_DOMAIN': f"{os.environ.get('AWS_STORAGE_BUCKET_NAME')}.s3.amazonaws.com",
    'STATIC_URL': f"https://{os.environ.get('AWS_STORAGE_BUCKET_NAME')}.s3.amazonaws.com/static/",
    'MEDIA_URL': f"https://{os.environ.get('AWS_STORAGE_BUCKET_NAME')}.s3.amazonaws.com/media/",
}

# ============================================================================
# GOOGLE CLOUD PLATFORM
# ============================================================================

GCP_SETTINGS = {
    'ALLOWED_HOSTS': ['.appspot.com', '.your-domain.com'],
    'SECURE_SSL_REDIRECT': True,
    'SECURE_PROXY_SSL_HEADER': ('HTTP_X_FORWARDED_PROTO', 'https'),
    'SESSION_COOKIE_SECURE': True,
    'CSRF_COOKIE_SECURE': True,
    'SECURE_HSTS_SECONDS': 31536000,
    'SECURE_HSTS_INCLUDE_SUBDOMAINS': True,
    'SECURE_HSTS_PRELOAD': True,
    
    # Cloud SQL
    'DATABASES': {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('DB_NAME'),
            'USER': os.environ.get('DB_USER'),
            'PASSWORD': os.environ.get('DB_PASSWORD'),
            'HOST': f"/cloudsql/{os.environ.get('CLOUD_SQL_CONNECTION_NAME')}",
            'PORT': '',
        }
    }
}

# ============================================================================
# CLOUDFLARE CONFIGURATION
# ============================================================================

CLOUDFLARE_SETTINGS = {
    'SECURE_PROXY_SSL_HEADER': ('HTTP_CF_VISITOR', '{"scheme":"https"}'),
    'SECURE_SSL_REDIRECT': True,
    'SESSION_COOKIE_SECURE': True,
    'CSRF_COOKIE_SECURE': True,
    'SECURE_HSTS_SECONDS': 31536000,
    'SECURE_HSTS_INCLUDE_SUBDOMAINS': True,
    'SECURE_HSTS_PRELOAD': True,
    
    # Cloudflare specific headers
    'SECURE_BROWSER_XSS_FILTER': True,
    'SECURE_CONTENT_TYPE_NOSNIFF': True,
    'X_FRAME_OPTIONS': 'DENY',
}

# ============================================================================
# VPS/DEDICATED SERVER (NGINX + GUNICORN)
# ============================================================================

VPS_SETTINGS = {
    'ALLOWED_HOSTS': ['your-domain.com', 'www.your-domain.com'],
    'SECURE_SSL_REDIRECT': True,
    'SECURE_PROXY_SSL_HEADER': ('HTTP_X_FORWARDED_PROTO', 'https'),
    'SESSION_COOKIE_SECURE': True,
    'CSRF_COOKIE_SECURE': True,
    'SECURE_HSTS_SECONDS': 31536000,
    'SECURE_HSTS_INCLUDE_SUBDOMAINS': True,
    'SECURE_HSTS_PRELOAD': True,
    'SECURE_BROWSER_XSS_FILTER': True,
    'SECURE_CONTENT_TYPE_NOSNIFF': True,
    'X_FRAME_OPTIONS': 'DENY',
    
    # Static files
    'STATIC_ROOT': '/var/www/davegames/staticfiles/',
    'MEDIA_ROOT': '/var/www/davegames/media/',
    
    # Database
    'DATABASES': {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('DB_NAME', 'davegames_db'),
            'USER': os.environ.get('DB_USER', 'postgres'),
            'PASSWORD': os.environ.get('DB_PASSWORD'),
            'HOST': os.environ.get('DB_HOST', 'localhost'),
            'PORT': os.environ.get('DB_PORT', '5432'),
        }
    }
}

# ============================================================================
# DOCKER CONFIGURATION
# ============================================================================

DOCKER_SETTINGS = {
    'ALLOWED_HOSTS': ['*'],  # Configurar según el entorno
    'SECURE_SSL_REDIRECT': False,  # Manejar en el proxy reverso
    'SESSION_COOKIE_SECURE': True,
    'CSRF_COOKIE_SECURE': True,
    
    # Database
    'DATABASES': {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('POSTGRES_DB', 'davegames_db'),
            'USER': os.environ.get('POSTGRES_USER', 'postgres'),
            'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
            'HOST': os.environ.get('DB_HOST', 'db'),
            'PORT': os.environ.get('DB_PORT', '5432'),
        }
    }
}

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_deployment_settings(provider='development'):
    """
    Obtener configuraciones según el proveedor
    
    Args:
        provider (str): Proveedor de hosting
        
    Returns:
        dict: Configuraciones específicas del proveedor
    """
    providers = {
        'heroku': HEROKU_SETTINGS,
        'digitalocean': DIGITALOCEAN_SETTINGS,
        'aws': AWS_SETTINGS,
        'gcp': GCP_SETTINGS,
        'cloudflare': CLOUDFLARE_SETTINGS,
        'vps': VPS_SETTINGS,
        'docker': DOCKER_SETTINGS,
    }
    
    return providers.get(provider, {})

def apply_deployment_settings(settings_dict, provider='development'):
    """
    Aplicar configuraciones de despliegue a settings de Django
    
    Args:
        settings_dict (dict): Diccionario de settings de Django
        provider (str): Proveedor de hosting
    """
    deployment_settings = get_deployment_settings(provider)
    
    for key, value in deployment_settings.items():
        if key == 'MIDDLEWARE_ADDITIONS':
            # Agregar middleware adicional
            if 'MIDDLEWARE' in settings_dict:
                for middleware in value:
                    if middleware not in settings_dict['MIDDLEWARE']:
                        settings_dict['MIDDLEWARE'].insert(1, middleware)
        else:
            settings_dict[key] = value
    
    return settings_dict

# ============================================================================
# ENVIRONMENT DETECTION
# ============================================================================

def detect_environment():
    """
    Detectar automáticamente el entorno de despliegue
    
    Returns:
        str: Nombre del proveedor detectado
    """
    if 'DYNO' in os.environ:
        return 'heroku'
    elif 'APP_PLATFORM' in os.environ:
        return 'digitalocean'
    elif 'AWS_EXECUTION_ENV' in os.environ:
        return 'aws'
    elif 'GAE_ENV' in os.environ:
        return 'gcp'
    elif 'CF_RAY' in os.environ:
        return 'cloudflare'
    elif os.path.exists('/.dockerenv'):
        return 'docker'
    else:
        return 'vps'