##############################################################################
###                      DEFAULT SAVOY SETTINGS                            ###
###   These are the settings that should be added to your Django           ###
###   settings for use with Savoy. Not all are necessary for all apps.     ###
###   Read through them and figure out what you need and what you don't.   ###
##############################################################################  

# Set the current python path to include third party dependencies
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'third_party'))

# Select savoy.core.profiles.models.Profile as the default user profile
AUTH_PROFILE_MODULE     = 'profiles.Profile'

# Make sure you have the Savoy pages middleware, as well as the pagination
# middleware in place.
MIDDLEWARE_CLASSES = (
  'django.middleware.common.CommonMiddleware',
  'django.contrib.sessions.middleware.SessionMiddleware',
  'django.contrib.auth.middleware.AuthenticationMiddleware',
  'savoy.core.pages.middleware.PageFallbackMiddleware',
  'pagination.middleware.PaginationMiddleware',
)

# Add the pages context processor to your TEMPLATE_CONTEXT_PROCESSORS.
TEMPLATE_CONTEXT_PROCESSORS = (
  'django.core.context_processors.auth',
  'django.core.context_processors.debug',
  'django.core.context_processors.i18n',
  'django.core.context_processors.media',
  'django.core.context_processors.request',
  'savoy.core.pages.context_processors.add_page',
)

# Add the core Savoy apps, plus the contrb Savoy apps you with to use,
# to your INSTALLED_APPS setting.
INSTALLED_APPS = (

  # Put any of your own apps here.
  # 'myproject.myapp',

  # These Savoy contrib apps are entirely
  # optional.
  'savoy.contrib.aggregator',
  'savoy.contrib.blogs',
  'savoy.contrib.bookmarks',
  'savoy.contrib.code_samples',
  'savoy.contrib.comments',
  'savoy.contrib.events',
  'savoy.contrib.fragments',
  'savoy.contrib.galleries',
  'savoy.contrib.inlines',
  'savoy.contrib.podcasts',
  'savoy.contrib.portfolio',
  'savoy.contrib.quotations',
  'savoy.contrib.search',
  'savoy.contrib.sections',
  'savoy.contrib.statuses',
  
  # These Savoy core apps are required, as 
  # Savoy contrib apps expect them.
  'savoy.core.pages',
  'savoy.core.template_utils',
  'savoy.core.media',
  'savoy.core.people',
  'savoy.core.profiles',
  'savoy.core.organizations',
  'savoy.core.geo',

  # These third-party apps are optional, and Savoy
  # is distributed with them.
  'contact_form',
  
  # These third-party apps are required, and Savoy
  # is distributed with them.
  'pagination',
  'typogrify',
  'tagging',
  
  # These django.contrib apps are optional, but recommended. 
  # They are distributed with Django.
  'django.contrib.humanize',
  'django.contrib.admin',
  'django.contrib.admindocs',
  'django.contrib.redirects',
  
  
  # These django.contrib apps are required. They are
  # distributed with Django.
  'django.contrib.auth',
  'django.contrib.contenttypes',
  'django.contrib.sessions',
  'django.contrib.sites',
  'django.contrib.markup',
)

# For blogs app
USE_SINGLE_BLOG_URLS    = True        # If True, URL to blog will be /blog/ rather than /blog/blog-slug.

# For imported content. All content imported from third-party systems (Flickr,
# Delicious, etc.) will have its time automatically converted to this time zone.

UTC_OFFSET              = -8           # US/Pacific

# API Keys, etc. for various importers.
YAHOO_API_KEY           = ""          # Your Yahoo API key
GOOGLE_MAPS_API_KEY     = ""          # Your Google maps API key
UPCOMING_API_KEY        = ""          # Your Upcoming API key
UPCOMING_TOKEN          = ""          # Your Upcoming token
UPCOMING_USERNAME       = ""          # Your Upcoming username
DELICIOUS_USERNAME      = ""          # Your del.icio.us username
DELICIOUS_PASSWORD      = ""          # Your del.icio.us password
MAGNOLIA_API_KEY        = ""          # Your ma.gnolia API key
MAGNOLIA_USERNAME       = ""          # Your ma.gnolia username
FLICKR_API_KEY          = ""          # Your Flickr API key
FLICKR_API_SECRET       = ""          # Your Flickr API secret
FLICKR_USERID           = ""          # Your Flickr UserID (i.e. 33956054@N00)
FLICKR_USERNAME         = ""          # Your Flickr username
TWITTER_USERNAME        = ""          # Your Twitter username
TWITTER_PASSWORD        = ""          # Your Twitter password
URBAN_MAPPING_API_KEY   = ""          # Your Urban Mapping API key

# To use Akismet spam protection in comments, you'll need an Akismet API key.
AKISMET_USER_AGENT      = "Savoy 1.0"
AKISMET_API_KEY         = ""          # Your Akismet API Key
AKISMET_SITE_URL        = ""          # Your site's URL

# For the search app: Add each model you'd like to search. Each entry
# must contain "model" and "fields" keys. The "manager" key is optional.
# All models listed will be have results returned in searches via the search
# app. If a "manager" is specificed, the search app will only return results
# from the model which are returned in a Object.manager.all() query.
#
# EXAMPLE:
#
# SEARCH_MODELS = [
#   { 
#     'model': 'blogs.entry',
#     'fields': ['title', 'tags'],
#     'manager': 'live_entries',
#   },
#   { 
#     'model': 'bookmarks.bookmark',
#     'fields': ['title', 'tags'],
#   },
# ]

SEARCH_MODELS = []


# For the aggregator app: Add each model you'd like to include. Each entry
# must contain "model", "date_field", and "default" keys. The "manager"
# key is optional. All models listed will be "followed" by the aggregator
# app. If a "manager" is specificed, the aggregator app will only follow
# items from the model which are returned in a Object.manager.all() query.
# Also takes an optional "search_fields" key. If you wish to use the aggregator
# app's search view (instead of the search app), enter "search_fields" for
# all models.
#
# EXAMPLE:
#
# AGGREGATOR_MODELS = [
#   { 
#     'model': 'blogs.entry',
#     'date_field': 'date_published',
#     'default': 'enabled',
#     'manager': 'live_entries',
#     'search_fields': ['title', 'tags'],
#   },
#   { 
#     'model': 'bookmarks.bookmark',
#     'date_field': 'date_published',
#     'default': 'enabled',
#     'search_fields': ['title', 'tags'],
#   },
# ]

AGGREGATOR_MODELS = []