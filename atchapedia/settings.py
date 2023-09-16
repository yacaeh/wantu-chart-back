from pathlib     import Path

import pymysql

pymysql.install_as_MySQLdb()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
from os import path


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-f=msjy)w)(b&_iuwx(c(i9%%04n!3!t_a@bnyv=fe(%h=c3pu5'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bulk_update_or_create',
    'corsheaders',
    'users',
    'movies',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'atchapedia.urls'
BASE_DIR = path.dirname(path.dirname(path.abspath(__file__)))

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
      # The `GenreAdmin` class is registering the `Genre` model with the Django admin site and
      # customizing its display in the admin interface. It specifies the fields to be displayed in the
      # list view of the admin site for the `Genre` model. In this case, it displays the `id` and
      # `genre` fields.
        },
    },
]

WSGI_APPLICATION = 'atchapedia.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases


DATABASES = {
    'dev': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'wantu-pedia',
        'USER': 'wantu',
        'PASSWORD': 'wantu1234!',
        'HOST': 'localhost',
        'PORT': '3306',
    },
    'production': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'wantu-pedia',
        'USER': 'wantu',
        'PASSWORD': 'wantu1234!',
        'HOST': 'artvez.candlzmf9vc7.ap-northeast-2.rds.amazonaws.com',
        'PORT': '3306',
    },
}


if DEBUG is True :
    defaultDB = 'dev'
    STATICFILES_DIRS = [
        path.join(BASE_DIR, 'media')
    ]

else:
    defaultDB = 'production'
    STATIC_ROOT = path.join(BASE_DIR, 'static')

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators
DATABASES['default'] = DATABASES[defaultDB]

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#REMOVE_APPEND_SLASH_WARNING
APPEND_SLASH = False

##CORS
CORS_ORIGIN_ALLOW_ALL=True
CORS_ALLOW_CREDENTIALS=True

CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
)

CORS_ALLOW_HEADERS = (
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
		#만약 허용해야할 추가적인 헤더키가 있다면?(사용자정의 키) 여기에 추가하면 됩니다.
)
YOUTUBE_API_KEY="AIzaSyDlo1ez9E0Zh81kij8v4Ipx0NWVRrocx0w"
YOUTUBE_API_URL="https://www.googleapis.com/youtube/v3"
LOCAL_YOUTUBE_API_URL="http://localhost:8080"