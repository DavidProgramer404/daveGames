"""
Configuraciones SSL para DaveGames
Importar en settings.py según el entorno
"""

import os
from decouple import config


def configure_ssl_development():
    """Configuración SSL para desarrollo local"""
    return {
        "SECURE_SSL_REDIRECT": False,  # No forzar HTTPS en desarrollo
        "SESSION_COOKIE_SECURE": False,
        "CSRF_COOKIE_SECURE": False,
        "SECURE_HSTS_SECONDS": 0,
        "SECURE_HSTS_INCLUDE_SUBDOMAINS": False,
        "SECURE_HSTS_PRELOAD": False,
    }


def configure_ssl_production():
    """Configuración SSL para producción"""
    return {
        # Forzar HTTPS
        "SECURE_SSL_REDIRECT": True,
        # Configuración de proxy SSL (para Nginx, Heroku, etc.)
        "SECURE_PROXY_SSL_HEADER": ("HTTP_X_FORWARDED_PROTO", "https"),
        # HTTP Strict Transport Security (HSTS)
        "SECURE_HSTS_SECONDS": 31536000,  # 1 año
        "SECURE_HSTS_INCLUDE_SUBDOMAINS": True,
        "SECURE_HSTS_PRELOAD": True,
        # Cookies seguras
        "SESSION_COOKIE_SECURE": True,
        "CSRF_COOKIE_SECURE": True,
        "SESSION_COOKIE_HTTPONLY": True,
        "CSRF_COOKIE_HTTPONLY": True,
        # Configuración adicional de seguridad
        "SECURE_BROWSER_XSS_FILTER": True,
        "SECURE_CONTENT_TYPE_NOSNIFF": True,
        "SECURE_REFERRER_POLICY": "strict-origin-when-cross-origin",
        "X_FRAME_OPTIONS": "DENY",
        # Configuración de Content Security Policy (CSP)
        "CSP_DEFAULT_SRC": ["'self'"],
        "CSP_STYLE_SRC": [
            "'self'",
            "'unsafe-inline'",
            "https://cdn.jsdelivr.net",
            "https://fonts.googleapis.com",
            "https://cdnjs.cloudflare.com",
        ],
        "CSP_SCRIPT_SRC": [
            "'self'",
            "https://cdn.jsdelivr.net",
            "https://cdnjs.cloudflare.com",
        ],
        "CSP_FONT_SRC": [
            "'self'",
            "https://fonts.gstatic.com",
            "https://cdnjs.cloudflare.com",
        ],
        "CSP_IMG_SRC": ["'self'", "data:", "https:"],
        "CSP_CONNECT_SRC": ["'self'"],
    }


def get_ssl_settings(debug=True):
    """
    Obtener configuraciones SSL según el entorno

    Args:
        debug (bool): True para desarrollo, False para producción

    Returns:
        dict: Configuraciones SSL
    """
    if debug:
        return configure_ssl_development()
    else:
        return configure_ssl_production()


# Configuraciones específicas por proveedor
HEROKU_SSL_SETTINGS = {
    "SECURE_PROXY_SSL_HEADER": ("HTTP_X_FORWARDED_PROTO", "https"),
    "SECURE_SSL_REDIRECT": True,
    "SESSION_COOKIE_SECURE": True,
    "CSRF_COOKIE_SECURE": True,
}

CLOUDFLARE_SSL_SETTINGS = {
    "SECURE_PROXY_SSL_HEADER": ("HTTP_CF_VISITOR", '{"scheme":"https"}'),
    "SECURE_SSL_REDIRECT": True,
    "SESSION_COOKIE_SECURE": True,
    "CSRF_COOKIE_SECURE": True,
}

AWS_SSL_SETTINGS = {
    "SECURE_PROXY_SSL_HEADER": ("HTTP_X_FORWARDED_PROTO", "https"),
    "SECURE_SSL_REDIRECT": True,
    "SESSION_COOKIE_SECURE": True,
    "CSRF_COOKIE_SECURE": True,
    "USE_TZ": True,
}

NGINX_SSL_SETTINGS = {
    "SECURE_PROXY_SSL_HEADER": ("HTTP_X_FORWARDED_PROTO", "https"),
    "SECURE_SSL_REDIRECT": True,
    "SESSION_COOKIE_SECURE": True,
    "CSRF_COOKIE_SECURE": True,
}
