"""
Django settings for marchingtbirds project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
DJ_PROJECT_DIR = os.path.dirname(__file__)
BASE_DIR = os.path.dirname(DJ_PROJECT_DIR)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!iudke*hi8vo#qyntq5yxm+p2itkuqg-m@bo8o%+cbnq(h%@@-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True
TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]

#MEDIA_ROOT = BASE_DIR + '/media'

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    #'django.contrib.sites',
    'tinymce',
    'marchingtbirds',
    'nest',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'marchingtbirds.urls'

WSGI_APPLICATION = 'marchingtbirds.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
if "OPENSHIFT_POSTGRESQL_DB_USERNAME" in os.environ:

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME':     os.environ['OPENSHIFT_APP_NAME'],
            'USER':     os.environ['OPENSHIFT_POSTGRESQL_DB_USERNAME'],
            'PASSWORD': os.environ['OPENSHIFT_POSTGRESQL_DB_PASSWORD'],
            'HOST':     os.environ['OPENSHIFT_POSTGRESQL_DB_HOST'],
            'PORT':     os.environ['OPENSHIFT_POSTGRESQL_DB_PORT'],
        }
    }

else:

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            # GETTING-STARTED: change 'db.sqlite3' to your sqlite3 database:
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'static')
#STATIC_ROOT = 'staticfiles'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
    #'/var/www/static/',
)

# Media files
MEDIA_ROOT = '/static/'
MEDIA_URL = '/media/'

# TinyMCE
TINYMCE_DEFAULT_CONFIG = {
    'theme': "advanced",
    'theme_advanced_layout_manager': "SimpleLayout",
    'theme_advanced_buttons1': "paste, removeformat, separator, undo, redo, |, fontsizeselect, bold, italic, underline, strikethrough, |, justifyleft, justifycenter, justifyright, |, bullist, numlist, blockquote, image, |, link, unlink, |, code, help",
    'theme_advanced_buttons2': "",
    'theme_advanced_buttons3': "",
    'theme_advanced_statusbar_location': "none",
    'width': "60%",
    'height': "200",
    'cleanup_on_startup': True,
}

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
# not sure what the hell this is!
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Suit
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP

TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
)

SUIT_CONFIG = {
    # header
    'ADMIN_NAME': 'Marching Thunderbirds Admin',
    'HEADER_DATE_FORMAT': 'l, F j, Y',
    'HEADER_TIME_FORMAT': 'g:i:s A',

    # forms
    'SHOW_REQUIRED_ASTERISK': True,  # Default True
    'CONFIRM_UNSAVED_CHANGES': True, # Default True

    # menu
    'SEARCH_URL': '',
    #'MENU_ICONS': {
    #    'auth': 'icon-lock',
    #},
    'MENU_OPEN_FIRST_CHILD': True, # Default True
    #'MENU_EXCLUDE': (),
    'MENU': (
        #'-',
        #{'label':'Student list', 'icon':'icon-user', 'permissions':'nest.change_student', 'models':('nest.student',)},
        #{'label':'Uniform assignments', 'icon':'icon-pencil', 'models':('nest.uniform',)},
        #{'label':'Uniform database', 'icon':'icon-book', 'models':('nest.jacket','nest.pants','nest.hat','nest.raincoat',)},
        #{'label':'Other NEST options', 'icon':'icon-plus', 'permissions':'nest.change_authenticationcode', 'models':('nest.authenticationcode','nest.bulletin',),},
        '-',
        {'app':'marchingtbirds','label':'Website tools', 'icon':'icon-globe', 'models':('newspost','coverphoto','staffmember','currentfieldshow','historyrecord',)},
        {'app':'auth', 'label':'User management', 'models':('user','group')},
    ),

    # misc
    #'LIST_PER_PAGE': 20
}
