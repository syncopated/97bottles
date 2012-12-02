from django.http import Http404

from savoy.contrib.podcasts.models import Show, Episode

def show_detail(request, slug):
  from django.views.generic.list_detail import object_detail
  return object_detail(
    request, 
    queryset=Show.objects.all(),
    slug_field='slug',
    slug=slug,
    template_object_name='show',
  )


def episode_detail(request, show_slug, month, year, day, slug):
  from django.views.generic.list_detail import object_detail
  
  try:
    show = Show.objects.get(slug=show_slug)
    episode = Episode.objects.get(slug=slug, show=show)
  except (Episode.DoesNotExist, Show.DoesNotExist):
    raise Http404
  
  extra_context={ 
    'show' : show,
  }

  return object_detail(
    request, 
    queryset=Episode.objects.filter(show__slug=show_slug),
    slug_field='slug',
    slug=slug,
    template_object_name='episode',
    extra_context=extra_context,
  )
  
  
def episode_archive(request, show_slug, month=False, year=False, day=False):
  from django.views.generic.date_based import archive_day, archive_month, archive_year, archive_index

  try:
    show = Show.objects.get(slug=show_slug)
    episodes = show.episode_set.all()
  except Show.DoesNotExist:
    raise Http404
  
  if day:
    return archive_day(
      request, 
      queryset=episodes,
      date_field='date_published',
      template_object_name='episode',
      allow_empty = True,
      month = month,
      day = day,
      year = year,
    )
  elif month:
    return archive_month(
      request, 
      queryset=episodes,
      date_field='date_published',
      template_object_name='episode',
      allow_empty = True,
      month = month,
      year = year,
    )
  elif year:
    return archive_year(
      request, 
      queryset=episodes,
      date_field='date_published',
      template_object_name='episode',
      allow_empty = True,
      year = year,
    )
  else:
    return archive_index(
      request, 
      queryset=episodes,
      date_field='date_published',
      template_object_name='episode',
      allow_empty = True,
    )