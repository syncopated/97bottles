from django.contrib.auth.models import User
from django.core.cache import cache

def add_top_contributors_and_noobs(request):
  noobs = cache.get('noobs')
  if not noobs:
    cache.add('noobs', User.objects.all().order_by('-date_joined')[:12], 600)
    noobs = cache.get('noobs')
  top_contributors = cache.get('top_contributors')
  if not top_contributors:
    cache.add('top_contributors', User.objects.all().order_by('-info__contribution_score')[:12], 600)
    top_contributors = cache.get('top_contributors')
  return {'top_contributors': top_contributors, 'noobs': noobs }
