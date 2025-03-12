from pathlib import Path
import os
from datetime import timedelta
# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent
# Security settings
SECRET_KEY = 'django-insecure-a$qqb^o#l+i#ann+&so^9(()+)%j!5i_i#@v=vm)^z1okh5^rw'
DEBUG = True
ALLOWED_HOSTS = ["*"]
# Installed apps
INSTALLED_APPS = [
    'corsheaders',  # Keep CORS at the top
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'store',
    'rest_framework',
    'rest_framework.authtoken',
]
# Middleware (Fixed duplicate CORS middleware)
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Ensure CORS middleware is placed first
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
# CORS Configuration (Fixed conflicts)
CORS_ALLOW_ALL_ORIGINS = True  # Explicitly disable wildcard origins
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # React frontend
]
CORS_ALLOW_CREDENTIALS = True  # Allow cookies and authentication headers
CORS_ALLOW_HEADERS = [
    "content-type",
    "authorization",
    "x-csrftoken",
]  # Ensure necessary headers are allowed
# Django Rest Framework Configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',  # JWT Auth
        'rest_framework.authentication.TokenAuthentication',  # Token-based Auth
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
}
# JWT Token Configuration
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=365 * 10),  # Tokens valid for 10 years
    'REFRESH_TOKEN_LIFETIME': timedelta(days=365 * 20),  # Refresh tokens valid for 20 years
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
}
# URL and template settings
ROOT_URLCONF = 'ecommerce.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'store', 'templates')],
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
# WSGI application
WSGI_APPLICATION = 'ecommerce.wsgi.application'
# Database settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
# Authentication backend settings
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]
# CSRF settings (Fixed trusted origins)
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:3000',
    'http://127.0.0.1:8000',
]
# Static and media files settings
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# Password validation settings
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
# Login and logout redirects
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = '/login/'
LOGIN_URL = 'login'
# Auto field setting
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'









