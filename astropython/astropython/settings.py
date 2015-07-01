"""
Django settings for astropython project.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/

"""

from config import *
from spirit.settings import *
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/
# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY='cc*u4n__@&=^3x=hoyu-ndg(l^1^_4o72)bs4jt#5a#ewqhq7d'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

# Application definition

#Do not change the order of installed apps

INSTALLED_APPS += (
    'taggit', # Easy tagging functionality
    'secretballot',
    'crispy_forms',
    'compressor',
    'watson',
    'django.contrib.sites',
    'moderation', # Adding moderations
    'main',
    'social.apps.django_app.default', #Social  Authentication
)

MIDDLEWARE_CLASSES += (
    'secretballot.middleware.SecretBallotIpUseragentMiddleware',
    'watson.middleware.SearchContextMiddleware',
    )

ROOT_URLCONF = 'astropython.urls'

WSGI_APPLICATION = 'astropython.wsgi.application'

TEMPLATES[0]['OPTIONS']['context_processors'] += (
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
)

TEMPLATES[0]['OPTIONS']['loaders'] = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    )


#Add social auth options here
AUTHENTICATION_BACKENDS += (
    'social.backends.google.GoogleOAuth2',
    'social.backends.github.GithubOAuth2',
    'social.backends.yahoo.YahooOAuth',
    'social.backends.facebook.FacebookOAuth2',
    'social.backends.twitter.TwitterOAuth',
)

#Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

LANGUAGE_CODE = 'en-us'

USE_I18N = True

USE_L10N = True

USE_TZ = False

SITE_ID =1

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Static and Media files configuration (CSS, JavaScript, Images)

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static", "media")

STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static", "static_root")

STATICFILES_DIRS = (
    os.path.join(os.path.dirname(BASE_DIR), "static", "static_files"),
)

TEMPLATES[0]['DIRS'] = [
    os.path.join(BASE_DIR, 'templates'),
]

#States of a post
STATE_CHOICES = (
	('raw', 'raw'),
	('submitted', 'submitted'),
 )

INPUT_CHOICES = (
	('WYSIWYG', 'WYSIWYG'),
	('Markdown', 'Markdown'),
 )

CRISPY_TEMPLATE_PACK = 'bootstrap3'
