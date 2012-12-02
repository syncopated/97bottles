import datetime
import time

from django.http import Http404, HttpResponseRedirect
from django.template.loader import get_template
from django.template.defaultfilters import slugify
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django import forms
from django.forms.models import ModelChoiceField, model_to_dict
from django.conf import settings
from django.utils.encoding import force_unicode

from savoy.utils.slugs import get_unique_slug_value
from savoy.contrib.blogs.models import Blog, Entry
from savoy.core.people.models import Person

def blog_entry_detail(request, month, year, day, slug, blog_slug=None):
  from django.views.generic.list_detail import object_detail
  
  if settings.USE_SINGLE_BLOG_URLS and not blog_slug:
    try:
      blog_slug=Blog.objects.all()[0].slug
    except:
      raise Http404

  blog    = get_object_or_404(Blog, slug=blog_slug)
  entries = Entry.live_entries.filter(blogs=blog)
  entry   = get_object_or_404(entries, slug=slug)

  try:
      template = get_template('blogs/entries/%s.html' % entry.id)
      template = 'blogs/entries/%s.html' % str(entry.id)
  except:
      template = 'blogs/entry_detail.html'
  
  extra_context={ 
    'blog' : blog,
  }
  
  return object_detail(
    request, 
    queryset=entries,
    slug_field='slug',
    slug=slug,
    template_name=template,
    template_object_name='entry',
    extra_context=extra_context,
  )    


def blog_archive_index(request, blog_slug=None):
  from django.views.generic.date_based import archive_index
  
  if settings.USE_SINGLE_BLOG_URLS and not blog_slug:
    try:
      blog_slug=Blog.objects.all()[0].slug
    except:
      raise Http404
    
  blog    = get_object_or_404(Blog, slug=blog_slug)
  entries = Entry.live_entries.filter(blogs=blog)
    
  extra_context={ 
    'blog' : blog,
  }
  
  return archive_index(
    request,
    queryset=entries,
    date_field='date_published',
    num_latest = 30,
    allow_empty=True,
    extra_context=extra_context,
  )
    

def blog_archive_year(request, year, blog_slug=None):
  from django.views.generic.date_based import archive_year
  
  if settings.USE_SINGLE_BLOG_URLS and not blog_slug:
    try:
      blog_slug=Blog.objects.all()[0].slug
    except:
      raise Http404

  blog    = get_object_or_404(Blog, slug=blog_slug)
  entries = Entry.live_entries.filter(blogs=blog)
    
  extra_context={ 
      'blog' : blog,
  }
    
  return archive_year(
    request,
    year=year,
    queryset=entries,
    date_field='date_published',
    make_object_list=True,
    allow_empty=True,
    extra_context=extra_context,
    template_object_name='entry',
  )

def blog_archive_month(request, year, month, blog_slug=None):
  from django.views.generic.date_based import archive_month

  if settings.USE_SINGLE_BLOG_URLS and not blog_slug:
    blog_slug=Blog.objects.all()[0].slug

  blog    = get_object_or_404(Blog, slug=blog_slug)
  entries = Entry.live_entries.filter(blogs=blog)

  extra_context={ 
    'blog' : blog,
  }

  return archive_month(
    request,
    year=year,
    month=month,
    queryset=entries,
    date_field='date_published',
    allow_empty=True,
    extra_context=extra_context,
    template_object_name='entry',
  ) 
    
def blog_archive_day(request, year, month, day, blog_slug=None):
  from django.views.generic.date_based import archive_day

  if settings.USE_SINGLE_BLOG_URLS and not blog_slug:
    try:
      blog_slug=Blog.objects.all()[0].slug
    except:
      raise Http404

  blog    = get_object_or_404(Blog, slug=blog_slug)
  entries = Entry.live_entries.filter(blogs=blog)

  extra_context={ 
    'blog' : blog,
  }

  return archive_day(
    request,
    year=year,
    month=month,
    day=day,
    queryset=entries,
    date_field='date_published',
    allow_empty=True,
    extra_context=extra_context,
    template_object_name='entry',
  )