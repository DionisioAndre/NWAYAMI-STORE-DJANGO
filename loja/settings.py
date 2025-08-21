from datetime import timedelta
from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-j%0x0n)jn@vfib31tmawt17bgn$=3x=_3y)=)yyt$v$!2r*#rm'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Add localhost and your render host to ALLOWED_HOSTS
ALLOWED_HOSTS = [
    '127.0.0.1', 
    'localhost', 
    'pagapouco.onrender.com', 
    'pagapouco1.vercel.app', 
    'loja2-django.onrender.com'
]

# Application definition
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
    'lojaApp',  # Certifique-se de que o nome da sua app esteja correto
    'whitenoise',  # Adicione o Whitenoise aqui
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Adicione isso no início da lista
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'loja.urls'

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

WSGI_APPLICATION = 'loja.wsgi.application'

<<<<<<< HEAD
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
=======
# Database
DATABASES = {
     'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'pagapoucobd',
        'USER': 'dionisio',
        'PASSWORD': 'PNRfiKzJDNoJO6Su6CYPNdIUPyjm3JRS',
        'HOST': 'dpg-cshhnnaj1k6c73980amg-a.singapore-postgres.render.com',
        'PORT': '5432',
>>>>>>> da0259fcee8726afb712a5afe2ca0ec21dfc0994
    }
}

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'  # Corrigido para incluir a barra inicial

# Diretório onde os arquivos estáticos serão coletados
STATIC_ROOT = BASE_DIR / 'staticfiles'  # ou qualquer caminho que você preferir

<<<<<<< HEAD
# Diretórios adicionais de arquivos estáticos
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'lojaApp', 'static'),
]

=======
>>>>>>> da0259fcee8726afb712a5afe2ca0ec21dfc0994
# Para garantir que os arquivos estáticos sejam servidos corretamente em produção
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'  # Se você estiver usando Whitenoise

# Media files (uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'  # Usando Path para consistência

# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

# Simple JWT settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}

# CORS settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000", 
    "https://pagapouco.onrender.com", 
    "https://pagapouco1.vercel.app", 
    "https://loja2-django.onrender.com"
]

# Custom User Model
AUTH_USER_MODEL = 'lojaApp.User1'
