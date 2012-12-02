from ninetyseven.settings import *

# Settings for Kenny's local dev enviroment.

DEBUG = False

# DATABASE_ENGINE     = 'sqlite3'                                   # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'ado_mssql'.
# DATABASE_NAME       = "/Users/jcroft/Development/python/ninetyseven/ninetyseven.db" # Or path to database file if using sqlite3.
# DATABASE_USER       = ''                                          # Not used with sqlite3.
# DATABASE_PASSWORD   = ''                                          # Not used with sqlite3.
# DATABASE_HOST       = ''                                          # Set to empty string for localhost. Not used with sqlite3.
# DATABASE_PORT       = ''                                          # Set to empty string for default. Not used with sqlite3.

DATABASE_ENGINE     = 'mysql'                                     # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'ado_mssql'.
DATABASE_NAME       = '97_dev'                          # Or path to database file if using sqlite3.
DATABASE_USER       = '97_d'                          # Not used with sqlite3.
DATABASE_PASSWORD   = 'm0nk3y'                                  # Not used with sqlite3.
DATABASE_HOST       = ''                                          # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT       = ''                                          # Set to empty string for default. Not used with sqlite3.


MEDIA_ROOT          = '/Users/kennymeyers/Code/static/'
MEDIA_URL           = 'http://localhost:8080/static'

LOCAL_DEV           = True
CACHE_BACKEND       = "dummy:///"

DESKTOP_TEMPLATE_DIRS = (
  '/Users/kennymeyers/Code/ninetyseven/templates/',
  '/Users/kennymeyers/Code/ninetyseven-dependencies/savoy/templates/',
)

MOBILE_TEMPLATE_DIRS = (
  "/Users/kennymeyers/Code/ninetyseven/templates_mobile/",
  "/Users/kennymeyers/Code/ninetyseven/templates/",
)

ADMIN_MEDIA_PREFIX  = 'http://localhost:8080/static/ninetyseven/django-admin/'