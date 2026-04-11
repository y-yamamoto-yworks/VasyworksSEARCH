"""
System Name: Vasyworks
Project Name: vacancy_search
Encoding: UTF-8
Copyright (C) 2020 - 2026 Yasuhiro Yamamoto
"""

import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '任意のキー'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'rest_framework',
    'django_bootstrap5',
    'django_filters',
    'corsheaders',
    'api',
    'building',
    'garage',
    'menu',
    'movie',
    'panorama',
    'rent_db',
    'room',
    'search',
    'search_map',
    'users',
    'viewer',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'vacancy_search.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'vacancy_search.wsgi.application'


# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'rent_db',
        'USER': 'yworks',
        'PASSWORD': '任意のパスワード',
        'HOST': 'DBサーバのIPアドレスなど',
        'PORT': '5432',
    }
}


# CSRF settings
CSRF_TRUSTED_ORIGINS = [
    # 公開用
    # 'https://vasyworks-search.yworks.net',
    # 'http://vasyworks-search.yworks.net',

    # 開発用
    'http://localhost:8000',
    'http://127.0.0.1:8000',
]


# CORS
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    # 本番用
    # 'https://vasyworks-search.yworks.net',
    # 'http://vasyworks-search.yworks.net',

    # 開発用
    'http://localhost:8000',
    'http://127.0.0.1:8000',
]
CORS_PREFLIGHT_MAX_AGE = 60 * 30  # 許可時間30分


# Authorization
AUTH_USER_MODEL = 'users.User'
AUTHENTICATION_BACKENDS = [
    'users.backends.UserBackEnd',
]
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/menu/'
LOGIN_ERROR_URL = '/login/'


# Password validation

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

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]


# Media files
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
}


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'


# Application settings
COMPANY_ID = 1      # 会社ID（会社マスタ参照用）
DEFAULT_PREF_ID = 26        # デフォルトの都道府県ID（未指定可）
DEFAULT_LAT = 35.011823     # デフォルトの緯度
DEFAULT_LNG = 135.768129        # デフォルトの経度
CONDO_FEES_NAME = '共益費'         # 共益費項目の表示名（共益費または管理費）
TAX_RATE = 0.1          # 消費税率
CACHE_FILE_URL = '/viewer/cache_media/'       # キャッシュファイルのURL
CACHE_FILE_DIR = os.path.join(BASE_DIR, 'media', 'cache')      # キャッシュファイルのディレクトリ
ORIGINAL_FILE_DIR = os.path.join(BASE_DIR, 'media', 'public')       # オリジナルファイルのディレクトリ
WATER_MARK_FONT_SIZE = 32   # キャッシュ画像の透かしのフォントサイズ
WATER_MARK_OPACITY = 64     # キャッシュ画像の透かしの不透明度
ORIGINAL_IMAGE_SIZE = 1920      # オリジナルキャッシュ画像の最大サイズ
THUMBNAIL_IMAGE_SIZE = 240      # サムネイルキャッシュ画像の最大サイズ
SMALL_IMAGE_SIZE = 320      # 小キャッシュ画像の最大サイズ
MEDIUM_IMAGE_SIZE = 640     # 中キャッシュ画像の最大サイズ
LARGE_IMAGE_SIZE = 1280     # 大キャッシュ画像の最大サイズ
