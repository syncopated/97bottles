import os

import savoy
from savoy.settings import *

SAVOY_ROOT = os.path.realpath(os.path.dirname(savoy.__file__))
PROJECT_ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__), ".."))

# Enter the names of anyone who should receive error e-mails here.
ADMINS = (
  ('Jeff Croft', 'jeff@blueflavor.com'),
#  ('Brian Rosner', 'brosner@gmail.com'),
)
MANAGERS=ADMINS

# Turn this off for production, on for development.
DEBUG = False

# Local time zone for this installation. Choices can be found here:
# http://www.postgresql.org/docs/8.1/static/datetime-keywords.html#DATETIME-TIMEZONE-SET-TABLE
# although not all variations may be possible on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Los_Angeles'

# Language code for this installation. All choices can be found here:
# http://www.w3.org/TR/REC-html40/struct/dirlang.html#langcodes
# http://blogs.law.harvard.edu/tech/stories/storyReader$15
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'c#25(g3xc(g6iirlbru#&n#qzp^s*#!-!^3%$@4o!cunz!my43'

ROOT_URLCONF = 'ninetyseven.urls'

MIDDLEWARE_CLASSES = (
  "ninetyseven.middleware.MobileMiddleware",
  "django.middleware.cache.UpdateCacheMiddleware",
  "django.middleware.gzip.GZipMiddleware",
  "django.middleware.common.CommonMiddleware",
  "django.contrib.sessions.middleware.SessionMiddleware",
  "django.contrib.auth.middleware.AuthenticationMiddleware",
  "django.middleware.doc.XViewMiddleware",
  "django.middleware.http.SetRemoteAddrFromForwardedFor",
  "savoy.core.middleware.exceptions.UserBasedExceptionMiddleware",
  # "savoy.core.middleware.access_control.LoginRequiredMiddleware",
  "pagination.middleware.PaginationMiddleware",
  # "debug_toolbar.middleware.DebugToolbarMiddleware",
  "savoy.core.pages.middleware.PageFallbackMiddleware",
  "django.middleware.cache.FetchFromCacheMiddleware",
)

TEMPLATE_CONTEXT_PROCESSORS = (
  "django.core.context_processors.auth",
  # "django.core.context_processors.debug",
  "django.core.context_processors.i18n",
  "django.core.context_processors.media",
  "django.core.context_processors.request",
  "savoy.core.pages.context_processors.add_page",
  "ninetyseven.context_processors.add_top_contributors_and_noobs",
)

INSTALLED_APPS = (
  'ninetyseven.apps.beers',
  'ninetyseven.apps.reviews',
  'ninetyseven.apps.taglines',
  'ninetyseven.apps.recommender',
  'ninetyseven.apps.tags',
  'ninetyseven.apps.relationships',
  'ninetyseven.apps.invites',
  'ninetyseven.apps.tell_a_friend',
  'ninetyseven.apps.preferences',
  'ninetyseven.apps.api',
  'ninetyseven.apps.search',
  
  'savoy.contrib.blogs',
  'savoy.contrib.fragments',
  'savoy.contrib.search',
  'savoy.contrib.sections',
  
  'savoy.core.pages',
  'savoy.core.template_utils',
  'savoy.core.media',
  'savoy.core.new.profiles',
  'savoy.core.people',
  'savoy.core.geo',
  
  'contact_form',
  
  'haystack',
  'pagination',
  'typogrify',
  'tagging',
  'categorization',
  'faves',
  'django_authopenid',
  # 'debug_toolbar',
  'timelines',
  'compress',
  # 'apibuilder',
  'registration',
  
  'django.contrib.admin',
  'django.contrib.admindocs',
  'django.contrib.auth',
  'django.contrib.contenttypes',
  'django.contrib.sessions',
  'django.contrib.sites',
  'django.contrib.markup',
  'django.contrib.humanize',
  'django.contrib.comments',
)


# NINETYSEVEN SETTINGS

AUTH_PROFILE_MODULE = 'profile.profile'
LOGIN_URL = "/account/signin/"
REQUIRE_LOGIN_PATH = "/account/signin/"
REQUIRE_LOGIN_ALLOWED_URL_PREFIXES = (
  '/static/',
  '/account/signup/',
  '/account/signout/',
  '/account/signin/complete/',
  '/account/register/',
  '/account/password/',
  '/pages/subscribed/',
  '/pages/unsubscribed/',
  '/feeds/',
)

LOGIN_REDIRECT_URL = '/'
ACCOUNT_ACTIVATION_DAYS = 15

FLICKR_API_KEY          = "24b4a7ec2aeec3b4e94c5e336b740e92"
FLICKR_API_SECRET       = "600c0c6f631f9a5b"
FLICKR_USERID           = "33956054@N00"
FLICKR_USERNAME         = "jcroft"
BEER_MAPPING_API_KEY    = "121472bae79985ca9a56fc707a59a1cb"

TIMELINES_MODELS = (
  { 
    'model': 'beers.beer',
    'date_field': 'date_created',
    'user_field': 'created_by',
    'default': 'enabled',
  },
  { 
    'model': 'beers.brewery',
    'date_field': 'date_created',
    'user_field': 'created_by',
    'default': 'enabled',
  },
  { 
    'model': 'beers.userrecommendation',
    'date_field': 'date_created',
    'user_field': 'from_user',
    'default': 'enabled',
  },
  { 
    'model': 'reviews.review',
    'date_field': 'date_created',
    'user_field': 'created_by',
    'default': 'enabled',
  },
  { 
    'model': 'faves.fave',
    'date_field': 'date_created',
    'user_field': 'user',
    'default': 'enabled',
    'manager': 'active_objects',
  },
  { 
    'model': 'relationships.relationship',
    'date_field': 'created',
    'user_field': 'from_user',
    'default': 'enabled',
  },
  { 
    'model': 'profiles.profile',
    'date_field': 'user.date_joined',
    'user_field': 'user',
    'default': 'enabled',
  },
)

HAYSTACK_SEARCH_ENGINE = 'whoosh'
HAYSTACK_WHOOSH_PATH = os.path.join(PROJECT_ROOT, "whoosh", "ninetyseven_index")

SEARCH_MODELS = [
  { 
    'model': 'tagging.tag',
    'fields': ['name'],
  },
  { 
    'model': 'beers.beer',
    'fields': ['name','characteristics','description','brewery__name'],
  },
  { 
    'model': 'beers.brewery',
    'fields': ['name','city__city'],
  },
  { 
    'model': 'profiles.profile',
    'fields': ['user__username','display_name', 'city__city'],
  },
]

# API SETTINGS

API_AUTH_REALM = "97 Bottles API"
API_LIMITS = {
  'anonymous': (100,500000),
  'authenticated': (100,500000),
  'staff': (None,500000),
  'superuser': (None,None),
}
API_DEFAULT_FORMAT = "json"
API_CACHE = {
  'anonymous': 3600,
  'authenticated': 600,
  'staff': 120,
  'superuser': 0,
}

# PRODUCTION-SPECIFIC SETTINGS

DATABASE_ENGINE     = 'mysql'                                     # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'ado_mssql'.
DATABASE_NAME       = '97bottles_97bottles'                       # Or path to database file if using sqlite3.
DATABASE_USER       = '97bottles'                                 # Not used with sqlite3.
DATABASE_PASSWORD   = '9ijhr43efgh'                               # Not used with sqlite3.
DATABASE_HOST       = '172.21.1.233'                              # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT       = ''                                          # Set to empty string for default. Not used with sqlite3.


MEDIA_ROOT          = os.path.join(PROJECT_ROOT, "static", "ninetyseven") + "/"
MEDIA_URL           = '/static/ninetyseven/'

ADMIN_MEDIA_PREFIX  = '/static/django-admin/'

CACHE_BACKEND                   = "memcached://127.0.0.1:11211/"
MOBILE_CACHE_KEY_PREFIX         = "97mobile"
DESKTOP_CACHE_KEY_PREFIX        = "97desktop"
CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True
CACHE_MIDDLEWARE_SECONDS        = 300

LOCAL_DEV           = False

EMAIL_HOST          = "173.45.224.196"
DEFAULT_FROM_EMAIL  = "info@97bottles.com"
SERVER_EMAIL        = "info@97bottles.com"
REPLY_EMAIL         = "info@97bottles.com"

TEMPLATE_DIRS = (
  os.path.join(PROJECT_ROOT, "templates"),
  os.path.join(SAVOY_ROOT, "templates"),
)

DESKTOP_TEMPLATE_DIRS = (
  os.path.join(PROJECT_ROOT, "templates"),
  os.path.join(SAVOY_ROOT, "templates"),
)

MOBILE_TEMPLATE_DIRS = (
  os.path.join(PROJECT_ROOT, "templates_mobile"),
  os.path.join(PROJECT_ROOT, "templates"),
  os.path.join(SAVOY_ROOT, "templates"),
)

COMPRESS = True
COMPRESS_AUTO = True
COMPRESS_CSS_FILTERS = None

COMPRESS_JS = {
    'jquery': {
        'external_urls': (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.3.2/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.7.1/jquery-ui.min.js',
        ),
    },
    'all': {
        'source_filenames': (
          "assets/js/jquery.ajaxQueue.js",
          "assets/js/jquery.autocomplete.js",
          "assets/js/jquery.dimensions.js",
          "assets/js/jquery.lightSwitch.js",
          "assets/js/jquery.liveSearch.js",
          "assets/js/97bottles.js"),
          'output_filename': 'assets/js/all_media.js',
    }
}
