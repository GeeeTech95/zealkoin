import dj_database_url
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '24q_*&tn+5k_*6h6$nsccghwwb#8b%v4i)1h(wd08_02_-(czt'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.humanize',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Users.apps.UsersConfig',
    'wallet.apps.WalletConfig',
    'company.apps.CompanyConfig',
    'myadmin.apps.MyadminConfig',
    'core.apps.CoreConfig',
    'crispy_forms',

    #3rd party
    'whitenoise.runserver_nostatic',
]

CRISPY_TEMPLATE_PACK = 'bootstrap4'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'zealkoin.urls'



TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR,'templates'), 
            os.path.join(BASE_DIR,'Users/templates'), 
            os.path.join(BASE_DIR,'templates/email'), 
            os.path.join(BASE_DIR,'templates/registration'),
            os.path.join(BASE_DIR,'templates/admin dashboard'),  
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'core.context.core',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'zealkoin.wsgi.application'

AUTH_USER_MODEL = 'Users.User'
# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

if DEBUG :
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
            "OPTIONS": {
                "timeout": 30,
            }
        },
        "OPTIONS": {
        # ...
        "timeout": 30,
        # ...
    }
    }

else :
    # Replace the SQLite DATABASES configuration with PostgreSQL:
    DATABASES = {
   'default': dj_database_url.config(default=os.environ.get('DATABASE_URL'))
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = []

AUTH_PASSWORD_VATORS = [
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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR,"media")

STATICFILES_DIRS = [

os.path.join(BASE_DIR,"static")
]

SITE_NAME = "loci Trade"

STATIC_ROOT = os.path.join(BASE_DIR,"asset")

STATIC_URL = '/static/'
#STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
 

LOGIN_REDIRECT_URL = 'login-redirect'

LOGOUT_REDIRECT_URL = 'index'
STATIC_URL = '/static/'

#EMAIL FOR ZOHO
EMAIL_HOST  = "smtp.zoho.com"
EMAIL_PORT = "587"
#for other emails 

EMAIL_HOST_USER_SUPPORT = "support@zealkoin.ltd"
DEFAULT_FROM_EMAIL  = "support@zealkoin.ltd"
EMAIL_HOST_PASSWORD = '#@Kyletech99zealkoin'
EMAIL_HOST_USER_ALERT = "transaction@zealkoin.ltd"


EMAIL_USE_TLS = True

SITE_NAME = "Zealkoin"
SITE_ADDRESS = "https://www.zealkoin.ltd/"

FREE_PLAN_DURATION = 2  #in days
SUBSCRIPTION_DURATION = 365   #in days

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

