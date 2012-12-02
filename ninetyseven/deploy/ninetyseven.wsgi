# ninetyseven.wsgi is configured to live in deploy.

import os
import sys

# redirect sys.stdout to sys.stderr for bad libraries like geopy that uses
# print statements for optional import exceptions.
# @@@ may not be needed
sys.stdout = sys.stderr

from os.path import abspath, dirname, join

sys.path.insert(0, abspath(join(dirname(__file__), "../../")))

from django.conf import settings
os.environ["DJANGO_SETTINGS_MODULE"] = "ninetyseven.settings"

from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()