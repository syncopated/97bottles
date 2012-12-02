from ninetyseven.settings import *

# DEVELOPMENT-SPECIFIC SETTINGS

DEBUG = True

DATABASE_ENGINE     = 'mysql'                                     # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'ado_mssql'.
DATABASE_NAME       = 'blueflavored_97d'                          # Or path to database file if using sqlite3.
DATABASE_USER       = 'blueflavored_97d'                          # Not used with sqlite3.
DATABASE_PASSWORD   = '230be260'                                  # Not used with sqlite3.
DATABASE_HOST       = ''                                          # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT       = ''                                          # Set to empty string for default. Not used with sqlite3.


MEDIA_ROOT          = '/home/blueflavored/webapps/static_ninetyseven_development/ninetyseven/'
MEDIA_URL           = 'http://dev.97bottles.com/static/ninetyseven/'

ADMIN_MEDIA_PREFIX  = 'http://dev.97bottles.com/static/django-admin/'

CACHE_BACKEND       = "memcached://127.0.0.1:11212/"

TEMPLATE_DIRS = (
  "/home/blueflavored/webapps/django_ninetyseven_development/ninetyseven/templates",
  "/home/blueflavored/webapps/django_ninetyseven_development/lib/python2.5/savoy/templates",
)

DESKTOP_TEMPLATE_DIRS = (
  "/home/blueflavored/webapps/django_ninetyseven_development/ninetyseven/templates",
  "/home/blueflavored/webapps/django_ninetyseven_development/lib/python2.5/savoy/templates",
)

MOBILE_TEMPLATE_DIRS = (
  "/home/blueflavored/webapps/django_ninetyseven_development/ninetyseven/templates_mobile",
  "/home/blueflavored/webapps/django_ninetyseven_development/lib/python2.5/savoy/templates",
)

INTERNAL_IPS = (
  '65.26.109.180',
)

HAYSTACK_WHOOSH_PATH = '/home/blueflavored/whoosh/ninetyseven_development_index'
