from django import template
from django.template import Library, Node
from django.conf import settings

from sorl.thumbnail.main import DjangoThumbnail, get_thumbnail_setting
from sorl.thumbnail.processors import dynamic_import, get_valid_options

register = Library()
  
def _get_path_from_url(url, root=settings.MEDIA_ROOT, url_root=settings.MEDIA_URL):
  """
  Returns a local filesystem path from a URL.
    
    settings.MEDIA_URL/images/something.jpg becomes settings.MEDIA_ROOT/images/something.jpg
    /images/something.jpg becomes settings.MEDIA_ROOT/images/something.jpg
  
  """
  if url.startswith(url_root):
    url = url[len(url_root):] # strip media url
  return settings.MEDIA_ROOT + url

@register.filter
def thumbnail(url, size='200x200',):
  """
  Given a URL (local or remote) to an image, creates a thumbnailed version of the image, saving
  it locally and then returning the URL to the new, smaller version. If the argument passed is a 
  single integer, like "200", will output a version of the image no larger than 200px wide. If the
  argument passed is two integers, like, "200x300", will output a cropped version of the image that
  is exactly 200px wide by 300px tall (cropped from the center).
  
    {{ story.get_leadphoto_url|thumbnail:"200" }}
    {{ story.get_leadphoto_url|thumbnail:"300x150" }}
  
  This filter is a wrapper around sorl-thumbnail that provides the remote image fetching, as well as
  backwards-compatibility with the previous Savoy thumbnail filter syntax.
  """
  import Image
  import os
  import urllib
  
  if not url == '':
    if not url.startswith(settings.MEDIA_URL):
      # If it's a remote image, download it and save it locally. This expects a
      # directory called img/thumbnailed in your MEDIA_ROOT
      download_filename = url.rsplit('/', 1)[1]                                               # Filename of image
      full_image_path = '%simg/thumbnailed/%s' % (settings.MEDIA_ROOT, download_filename)     # Local filesystem path where image should be saved
      relative_image_path = 'img/thumbnailed/%s' % (download_filename)                        # Path relative to MEDIA_ROOT
      local_image_url = '%simg/thumbnailed/%s' % (settings.MEDIA_URL, download_filename)      # Full URL to local copy of image
      if not os.path.exists(full_image_path):
        unsized_image = urllib.urlretrieve(url)                                               # Fetch original image
        insized_image = os.rename(unsized_image[0], full_image_path)                          # Move the image to the corect path.
      url = local_image_url
    else:
      full_image_path = _get_path_from_url(url)
      relative_image_path = full_image_path[len(settings.MEDIA_ROOT):]

    # Parse the size argument into tuples.
    try:
      # See if both height and width exist (i.e. "200x100")
      desired_width, desired_height = [int(x) for x in size.split('x')]
      new_size = (desired_width, desired_height)
      # Flag this image for cropping, since we want an explicit width AND height.
      crop = True
    except:
      # If only one exists ( i.e. "200"), use the value as the desired width. To do
      # this math, we need the original height of the image, so we must open the image.
      image = Image.open(_get_path_from_url(url))
      desired_width = int(size)
      new_size = (desired_width, image.size[1])
      crop = False
    DEBUG = get_thumbnail_setting('DEBUG')
    try:
      PROCESSORS = dynamic_import(get_thumbnail_setting('PROCESSORS'))
      VALID_OPTIONS = get_valid_options(PROCESSORS)
    except:
      if get_thumbnail_setting('DEBUG'):
        raise
      else:
        PROCESSORS = []
        VALID_OPTIONS = []
    try:
      if crop:
        opts = ['crop']
      else:
        opts = None
      thumbnail = DjangoThumbnail(relative_image_path, new_size, opts=opts, processors=PROCESSORS, **{})
      return thumbnail.absolute_url
    except:
      if DEBUG:
        raise
      else:
        return ''
  else:
    return ''

@register.filter
def thumbnail_images(value, size='200x200'):
  
  """
  Returns thumbnailed versions of image references found in HTML-link markup. 
  Relies on thumbnail filter and takes its same arguments.
    
    {{ object.body|markdown|thumbnail_images:"300" }}

  """
  from BeautifulSoup import BeautifulSoup


  soup = BeautifulSoup(value)
  images = soup.findAll('img')
  thumbs_found = False
  for img in images:
    image_url = img['src']
    thumb = thumbnail(image_url, size)
    img['src'] = thumb
    thumbs_found = True
  if thumbs_found:
    value = soup.renderContents()
  return value


@register.filter
def image_width(url):
  """
  Given an image URL, returns the image's width.

    {% person.photo|image_width %}

  """
  try:
    import Image
  except ImportError:
    try:
      from PIL import Image
    except ImportError:
      return ''

  try:
    if url.startswith("http://") or url.startswith("https://"):
      import urllib
      import cStringIO
      file  = urllib.urlopen(url)
      im    = cStringIO.StringIO(file.read())
      image = Image.open(im)
    else:
      image = Image.open(_get_path_from_url(url))
    return image.size[0]
  except:
    return ''



@register.filter
def image_height(url):
  """
  Given an image URL, returns the image's height.

    {% person.photo|image_height %}

  """
  try:
    import Image
  except ImportError:
    try:
      from PIL import Image
    except ImportError:
      return ''

  try:
    if url.startswith("http://") or url.startswith("https://"):
      import urllib
      import cStringIO
      file  = urllib.urlopen(url)
      im    = cStringIO.StringIO(file.read())
      image = Image.open(im)
    else:
      image = Image.open(_get_path_from_url(url))
    return image.size[1]
  except:
    return ''