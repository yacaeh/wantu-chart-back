from pathlib     import Path
import environ
import pymysql
from os import path

pymysql.install_as_MySQLdb()
env = environ.Env()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(
    env_file=path.join(BASE_DIR, '.env')
)
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-f=msjy)w)(b&_iuwx(c(i9%%04n!3!t_a@bnyv=fe(%h=c3pu5'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG')
REDIS_HOST = env('REDIS_HOST')
print(DEBUG, REDIS_HOST)

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'clearcache',
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
    'debug_toolbar',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
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

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_HOST,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases


DATABASES = {
    # 'dev': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': 'wantu-pedia',
    #     'USER': 'wantu',
    #     'PASSWORD': 'wantu1234!',
    #     'HOST': 'localhost',
    #     'PORT': '3306',
    # },
    'dev': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'wantu-chart',
        'USER': 'wantu',
        'PASSWORD': 'wantu1234!',
        'HOST': 'wantu.candlzmf9vc7.ap-northeast-2.rds.amazonaws.com',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4', # 테이블 생성 자동으로 해줄때 쓸 인코딩,, 이거안하면 밑에꺼해도 효과 엑스
            'use_unicode': True,
        },

    },
}


if DEBUG is True :
    defaultDB = 'dev'
    STATICFILES_DIRS = [
        path.join(BASE_DIR, 'media')
    ]

else:
    defaultDB = 'dev'
    STATICFILES_DIRS = [
        path.join(BASE_DIR, 'media')
    ]

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
INTERNAL_IPS = [
    '127.0.0.1',
]

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