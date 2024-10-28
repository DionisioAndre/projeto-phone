import dj_database_url
from whitenoise import WhiteNoise
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'sua-chave-secreta')
DEBUG = True  # Habilitar depuração durante o desenvolvimento
ALLOWED_HOSTS = ['localhost', '127.0.0.1']  # Permitir acesso local

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'rest_framework_simplejwt',
    'minha_app',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware','whitenoise.middleware.WhiteNoiseMiddleware',
]

# Remova ou comente as configurações de segurança para desenvolvimento
# SECURE_BROWSER_XSS_FILTER = True
# SECURE_CONTENT_TYPE_NOSNIFF = True
# SECURE_SSL_REDIRECT = not DEBUG  # Redireciona para HTTPS em produção
# SESSION_COOKIE_SECURE = not DEBUG  # Cookies seguros em produção
# CSRF_COOKIE_SECURE = not DEBUG  # Cookies CSRF seguros em produção
# SECURE_HSTS_SECONDS = 3600  # Ativar HSTS por 1 hora
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True
# SECURE_REFERRER_POLICY = 'no-referrer-when-downgrade'  # Política de Referência

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

ROOT_URLCONF = 'meu_projeto.urls'
DATABASES = {
    'default': dj_database_url.config(default='postgres://localhost')
}

# DATABASES = {
  'default': dj_database_url.config(default=os.getenv('DATABASE_URL'))
    }
#}

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000","pagapouco-app.herokuapp.com","vercel",
    # Adicione suas origens de produção aqui se necessário
]
CORS_ALLOW_METHODS = [
    "GET",
    "POST",
    "OPTIONS","PUT","DELETE"
]

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
WSGI_APPLICATION = 'meu_projeto.wsgi.application'
AUTH_USER_MODEL = 'minha_app.User'

# Remover a ativação do Heroku para desenvolvimento
# Ativar Heroku se necessário django_heroku.settings(locals())
