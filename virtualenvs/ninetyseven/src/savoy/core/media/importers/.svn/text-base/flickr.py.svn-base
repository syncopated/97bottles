from savoy.utils.path import append_third_party_path
append_third_party_path()


from decimal import Decimal
import datetime

from django.conf import settings
from django.template.defaultfilters import slugify
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_unicode
import flickrapi
from tagging.models import Tag

from savoy.core.media.models import *
from savoy.core.geo.models import *
from savoy.utils.text_parsing import unsmartypants
from savoy.utils.slugs import get_unique_slug_value

flickr = flickrapi.FlickrAPI(settings.FLICKR_API_KEY, settings.FLICKR_API_SECRET)


def truncate_tags(tags):
  tag_list = tags.split(' ')
  new_tag_list = []
  tag_count = len(tag_list)
  character_count = 0
  for tag in tag_list:
    length = len(tag) + 1
    character_count = character_count + length
    if character_count < 255:
      new_tag_list.append(tag)
  return " ".join(new_tag_list)


def create_or_update_geolocated_item(photo, latitude, longitude, country=None, city_name=None, county=None, state=None):
  try:
    # See if we already have a location for this photo.
    geo = GeolocatedItem.objects.get(content_type=ContentType.objects.get_for_model(Photo), object_id=photo.id)
  except:
    # If we don't, create a placeholder GeolocatedItem object.
    geo = GeolocatedItem(content_type=ContentType.objects.get_for_model(Photo), object_id=photo.id)
  
  # Update the GeolocatedItem object with the right values.
  geo.latitude = Decimal(latitude)
  geo.longitude = Decimal(longitude)
  geo.save()
  
  # Return the saved GeolocatedItem object.
  return geo
  

def create_or_update_flickr_comments(photo_id, savoy_photo, photo=False):
  from savoy.contrib.comments.models import Comment, FlickrComment
  
  try:
    flickr_comments = flickr.photos_comments_getList(photo_id=photo_id).comments[0]
  except:
    return
  try:
    savoy_flickr_photo = FlickrPhoto.objects.get(photo=savoy_photo)
  except:
    return
  comment_count = savoy_flickr_photo.comment_count
  try:
    for original_flickr_comment in flickr_comments.comment:
      try:
        # See if we already have this comment in our database
        flickr_comment = FlickrComment.objects.get(flickr_comment_id=original_flickr_comment['id'])
        comment = flickr_comment.comment
      except:
        flickr_comment = FlickrComment()
        comment = Comment()
  
      flickr_user                         = create_or_update_flickr_user(original_flickr_comment['author'])
      comment.content_type                = ContentType.objects.get_for_model(Photo)
      comment.object_id                   = savoy_photo.id
      comment.person                      = None
      comment.author_name                 = force_unicode(unsmartypants(original_flickr_comment['authorname']))
      comment.author_email_address        = 'user@flickr.com'
      comment.author_url                  = flickr_user.profile
      comment.author_ip_address           = '0.0.0.0'
      comment.author_user_agent_string    = ''
      comment.date_submitted              = datetime.datetime.fromtimestamp(int(original_flickr_comment['datecreate']))
      comment.body                        = force_unicode(unsmartypants(original_flickr_comment.elementText))
      comment.save()
  
      flickr_comment.comment              = comment
      flickr_comment.flickr_comment_id    = original_flickr_comment['id']
      flickr_comment.author               = flickr_user
      flickr_comment.url                  = original_flickr_comment['permalink']
      flickr_comment.save()
      print "\tSaved comment by " + str(comment.author_name)
  except:
    pass
      

def create_or_update_flickr_user(user_id):
  # Query the FlickrAPI for information about the user.
  flickr_person = flickr.people_getInfo(user_id=user_id).person[0]
  
  try:
    # See if we already have this user in our database.
    flickr_user = FlickrUser.objects.get(nsid=user_id)
  except:
    # If we don't, create a placeholder FlickrUser object.
    flickr_user = FlickrUser(nsid=user_id)
  
  # Update the FlickrUser object with the right values.
  flickr_user.username = flickr_person.username[0].elementText
  try:
    flickr_user.realname = flickr_person.realname[0].elementText
  except:
    flickr_user.realname = ''
  try:
    flickr_user.location = flickr_person.location[0].elementText
  except:
    flickr_user.location = ''
  flickr_user.photos = flickr_person.photosurl[0].elementText
  flickr_user.profile = flickr_person.profileurl[0].elementText
  flickr_user.photocount = int(flickr_person.photos[0].count[0].elementText)
  flickr_user.iconserver = int(flickr_person['iconserver'])
  flickr_user.iconfarm = int(flickr_person['iconfarm'])

  if flickr_person['isadmin'] == '1':
    flickr_user.isadmin = True
  else:
    flickr_user.isadmin = False

  if flickr_person['ispro'] == '1':
    flickr_user.ispro = True
  else:
    flickr_user.ispro = False

  flickr_user.save()
  
  # Return the saved FlickrUser object.
  return flickr_user

def create_or_update_flickr_note(note, flickr_photo):
  try:
    # See if we already have this note in our datbase.
    flickr_note = FlickrNote.objects.get(note_id=note['id'])
  except:
    # If we don't, create a placeholder FlickrNote object.
    flickr_note = FlickrNote(note_id=note['id'])
  
  # Update the FlickrNote object with the right values.
  flickr_note.flickr_photo = flickr_photo
  flickr_note.author = create_or_update_flickr_user(user_id=note['author'])
  flickr_note.text = note.elementText
  flickr_note.x = note['x']
  flickr_note.y = note['y']
  flickr_note.w = note['w']
  flickr_note.h = note['h']
  flickr_note.save()
  
  # Return the saved FlickrNote object.
  return flickr_note


def create_or_update_flickr_photo(photo_id, photo=False):
  # Set up initial varibles.
  flickr_update_date = None
  getInfo_done = False
  
  if photo:
    # If we already have the complete photo info (including last update date),
    # populate some variables with the appropriate values.
    flickr_update_date = datetime.datetime.fromtimestamp(int(photo['lastupdate']))
    tags = photo['tags']
  else:
    # If we don't already have the complete photo info (including last update date),
    # query some Flickr API methods to get the update date.
    photo = flickr.photos_getInfo(photo_id=photo_id).photo[0]
    flickr_update_date = photo.dates[0]['lastupdate']
    getInfo_done = True
  
  try:
    # See if we already have this photo in our database. If we do,
    # check the last update date. If it doesn't match with Flickr,
    # raise an Exception.
    flickr_photo = FlickrPhoto.objects.get(flickr_photo_id=photo_id)
    if not flickr_photo.date_updated == flickr_update_date:
      raise Exception
  except:
    # If we're here, it means the photo needs to be added or updated.
    # Query the FlickrAPI to get any remaining needed metadata.
    
    # We may have already done the getInfo method above. If so, don't
    # hit the Flickr API again.
    if not getInfo_done:
      photo = flickr.photos_getInfo(photo_id=photo_id).photo[0]
  
    # Gather up the geodata for this photo, if it exists.
    try:
      latitude = photo.location[0]['latitude']
      longitude = photo.location[0]['longitude']
    except:
      latitude = None
      longitude = None
    try:
      city_name = photo.location[0].locality[0].elementText
    except:
      city_name = None
    try:
      county = photo.location[0].county[0].elementText
    except:
      county = None
    try:
      region = photo.location[0].region[0].elementText
    except:
      region = None
    try:
      country = photo.location[0].country[0].elementText
    except:
      country = None
    
    # Try to get geo information from flickr.
    #try:
    #  geo = flickr.photos_geo_getLocation(photo_id=photo_id).photo[0]
    #  latitude = geo.location[0]['latitude']
    #  longitude = geo.location[0]['longitude']
    #  accuracy = int(geo.location[0]['accuracy'])
    #except:
    #  geo = False
    
    # Get the tags for the photo
    try:
      tag_xml = flickr.tags_getListPhoto(photo_id=photo_id).photo[0].tags[0].tag
      tag_list = []
      for tag in tag_xml:
        tag_list.append(tag.elementText)
      tags = " ".join(tag_list)
    except:
      pass
    
    
    # Get the information for the various photo sizes.
    sizes = flickr.photos_getSizes(photo_id=photo_id).sizes[0].size
    
    # Try to get the photo's EXIF data. If there isn't any, no worries.
    try:
      exif = flickr.photos_getExif(photo_id=photo_id).photo[0].exif
    except:
      exif = None
    
    
    try:
      # See if we already have this photo in our database.
      flickr_photo = FlickrPhoto.objects.get(flickr_photo_id=photo_id)
    except:
      # If we don't, create a placeholder FlickrPhoto object.
      flickr_photo = FlickrPhoto(flickr_photo_id=photo_id)
    
    # Set the various attributes of the FlickrPhoto object to the appropriate values.
    flickr_photo.secret = photo['secret']
    flickr_photo.server = int(photo['server'])
    flickr_photo.license = int(photo['license'])
    flickr_photo.rotation = int(photo['rotation'])
    try:
      flickr_photo.originalsecret = photo['originalsecret']
    except:
      flickr_photo.originalsecret = ""
    try:
      flickr_photo.originalformat = photo['originalformat']
    except:
      flickr_photo.originalformat = ""
    try:
      flickr_photo.media = photo['media']
    except:
      flickr_photo.media = ""
    flickr_photo.owner = create_or_update_flickr_user(user_id=photo.owner[0]['nsid'])

    if photo.visibility[0]['ispublic'] == '1':
      flickr_photo.ispublic = True
    else:
      flickr_photo.ispublic = False

    if photo.visibility[0]['isfriend'] == '1':
      flickr_photo.isfriend = True
    else:
      flickr_photo.isfriend = False

    if photo.visibility[0]['isfamily'] == '1':
      flickr_photo.isfamily = True
    else:
      flickr_photo.isfamily = False  

    if photo['isfavorite'] == '1':
      flickr_photo.isfavorite = True
    else:
      flickr_photo.isfavorite = False

    try:
      if photo.permissions[0]['permcomment'] == '1':
        flickr_photo.permcomment = True
      else:
        flickr_photo.permcomment = False    
      if photo.permissions[0]['permaddmeta'] == '1':
        flickr_photo.permaddmeta = True
      else:
        flickr_photo.permaddmeta = False
    except:
      pass

    try:
      if photo.editability[0]['cancomment'] == '1':
        flickr_photo.cancomment = True
      else:
        flickr_photo.cancomment = False
      if photo.editability[0]['canaddmeta'] == '1':
        flickr_photo.canaddmeta = True
      else:
        flickr_photo.canaddmeta = False
    except:
      pass

    flickr_photo.comment_count = photo.comments[0].elementText
    flickr_photo.date_posted = datetime.datetime.fromtimestamp(int(photo.dates[0]['posted']))
    flickr_photo.date_updated = datetime.datetime.fromtimestamp(int(photo.dates[0]['lastupdate']))
    flickr_photo.date_taken_granularity = int(photo.dates[0]['takengranularity'])
    flickr_photo.photo_page = photo.urls[0].url[0].elementText
    flickr_photo.flickr_photo_id = photo_id
  
    for size in sizes:
      if size['label'] == "Original":
        flickr_photo.original_image_url = size['source']
      if size['label'] == "Large":
        flickr_photo.large_image_url = size['source']
      if size['label'] == "Medium":
        flickr_photo.medium_image_url = size['source']
      if size['label'] == "Small":
        flickr_photo.small_image_url = size['source']
      if size['label'] == "Thumbnail":
        flickr_photo.thumbnail_image_url = size['source']
      if size['label'] == "Square":
        flickr_photo.square_image_url = size['source']
    
    # Create or update the Photo object (which is different from the FlickrPhoto object).
    savoy_photo = create_or_update_photo(photo=photo, sizes=sizes, tags=tags, exif=exif)
    flickr_photo.photo = savoy_photo
    
    # Save the FlickrPhoto object.
    try:
      if savoy_photo:
        flickr_photo.save()
      else:
        flickr_photo = None
    except:
      savoy_photo.delete()
      savoy_photo = None
    
    if flickr_photo and savoy_photo:
      try:
        # If there are notes for this photo, save them.
        for note in photo.notes[0].note:
          create_or_update_flickr_note(note=note, flickr_photo=flickr_photo)
      except:
        # If not, no worries.
        pass
    
      # Add or update and comments for this photo:
      create_or_update_flickr_comments(flickr_photo.flickr_photo_id, flickr_photo.photo, photo=photo)
    
      # If there is geo information for this photo, save it.
      if latitude and longitude:
        "updating geo item"
        GeolocatedItem.objects.create_or_update(flickr_photo.photo, location=(latitude, longitude))
      else:
        print "\tThis photo has no geo information."
    
    
  
  # Return the saved FlickrPhoto.
  return flickr_photo


def create_or_update_photo(photo, sizes, tags, exif):
  try:
    print "\nProcessing photo " + str(photo.title[0].elementText).encode('ascii', 'xmlcharrefreplace')
  except:
    print "\nProcessing photo (unable to print title...the photo's id is " + str(photo['id']) + ")"
  try:
    # See if we already have this photo in our database.
    savoy_photo = FlickrPhoto.objects.get(flickr_photo_id=photo['id']).photo
  except:
    # If we don't, create a placeholder Photo object for it.
    savoy_photo = Photo(slug=None)
  
  # Set the various attributes of the Photo object to the appropriate values.
  if photo.title[0].elementText != '':
    savoy_photo.title = force_unicode(photo.title[0].elementText)[:245]
  else:
    savoy_photo.title = 'Untitled'
  savoy_photo.description = force_unicode(photo.description[0].elementText)
  savoy_photo.date_created = photo.dates[0]['taken']
  savoy_photo.date_published = datetime.datetime.fromtimestamp(int(photo.dates[0]['posted']))
  
  if not savoy_photo.slug:
    proposed_slug = slugify(savoy_photo.title)
    savoy_photo.slug = get_unique_slug_value(Photo, proposed_slug)
  savoy_photo.tags = force_unicode(truncate_tags(tags))
  savoy_photo.aperture = ""
  
  for size in sizes:
    if size['label'] == "Original":
      savoy_photo.image_width = size['width']
      savoy_photo.image_height = size['height']
  if savoy_photo.image_width == None or savoy_photo.image_height == None:
    for size in sizes:
      if size['label'] == "Large":
        savoy_photo.image_width = size['width']
        savoy_photo.image_height = size['height']
  
  if exif:
    for tag in exif:
      
      if tag['label'] == 'Make':
        try:
          savoy_photo.make = tag.clean[0].elementText
        except:
          savoy_photo.make = tag.raw[0].elementText
          
      if tag['label'] == 'Model':
        try:
          savoy_photo.model = tag.clean[0].elementText
        except:
          savoy_photo.model = tag.raw[0].elementText
          
      if tag['label'] == 'Orientation':
        try:
          savoy_photo.orientation = tag.clean[0].elementText
        except:
          savoy_photo.orientation = tag.raw[0].elementText
          
      if tag['label'] == 'X-Resolution':
        try:
          savoy_photo.x_resolution_unit = tag.clean[0].elementText
        except:
          savoy_photo.x_resolution_unit = tag.raw[0].elementText
          
      if tag['label'] == 'Y-Resolution':
        try:
          savoy_photo.y_resolution = tag.clean[0].elementText
        except:
          savoy_photo.y_resolution = tag.raw[0].elementText
          
      if tag['label'] == 'Resolution Unit':
        try:
          savoy_photo.resolution_unit = tag.clean[0].elementText
        except:
          savoy_photo.resolution_unit = tag.raw[0].elementText
          
      if tag['label'] == 'Software':
        try:
          savoy_photo.software = tag.clean[0].elementText
        except:
          savoy_photo.software = tag.raw[0].elementText
          
      if tag['label'] == 'Host Computer':
        try:
          savoy_photo.host_computer = tag.clean[0].elementText
        except:
          savoy_photo.host_computer = tag.raw[0].elementText
          
      if tag['label'] == 'YCbCr Positioning':
        try:
          savoy_photo.ycbcr_positioning = tag.clean[0].elementText
        except:
          savoy_photo.ycbcr_positioning = tag.raw[0].elementText
          
      if tag['label'] == 'Exposure':
        try:
          savoy_photo.exposure = tag.clean[0].elementText
        except:
          savoy_photo.exposure = tag.raw[0].elementText
          
      if savoy_photo.aperture == "":
        if tag['label'] == 'Aperture':
          try:
            savoy_photo.aperture = tag.clean[0].elementText
          except:
            savoy_photo.aperture = tag.raw[0].elementText
            
      if tag['label'] == 'Shutter Speed':
        try:
          savoy_photo.shutter_speed = tag.clean[0].elementText
        except:
          savoy_photo.shutter_speed = tag.raw[0].elementText
          
      if tag['label'] == 'Exposure Bias':
        try:
          savoy_photo.exposure_bias = tag.clean[0].elementText
        except:
          savoy_photo.exposure_bias = tag.raw[0].elementText
          
      if tag['label'] == 'Metering Mode':
        try:
          savoy_photo.metering_mode = tag.clean[0].elementText
        except:
          savoy_photo.metering_mode = tag.raw[0].elementText
          
      if tag['label'] == 'Flash':
        try:
          savoy_photo.flash = tag.clean[0].elementText
        except:
          savoy_photo.flash = tag.raw[0].elementText
          
      if tag['label'] == 'Focal Length':
        try:
          savoy_photo.focal_length = tag.clean[0].elementText
        except:
          savoy_photo.focal_length = tag.raw[0].elementText
          
      if tag['label'] == 'Color Space':
        try:
          savoy_photo.color_space = tag.clean[0].elementText
        except:
          savoy_photo.color_space = tag.raw[0].elementText
          
      if tag['label'] == 'Sensing Method':
        try:
          savoy_photo.sensing_method = tag.clean[0].elementText
        except:
          savoy_photo.sensing_method = tag.raw[0].elementText
          
      if tag['label'] == 'Compression':
        try:
          savoy_photo.compression = tag.clean[0].elementText
        except:
          savoy_photo.compression = tag.raw[0].elementText

  # Save the Photo object.
  try:
    savoy_photo.save()
    print "\tSaved photo"
  except:
    print "\tERROR: Could not save photo"

  # Return the saved Photo object.
  return savoy_photo


def process_photos(flickr_photos):
  for photo in flickr_photos:
    photo_id = photo['id']
    savoy_flickr_photo = create_or_update_flickr_photo(photo_id=photo_id, photo=photo)

def process_all_public_photos_for_user(user_id):
  flickr_person = flickr.people_getInfo(user_id=user_id).person[0]
  photo_count = int(flickr_person.photos[0].count[0].elementText)
  page_count = photo_count / 500 + 1

  page = 1
  while page <= page_count:
    extras = "license, date_upload, date_taken, owner_name, icon_server, original_format, last_update, geo, tags, machine_tags"
    flickr_photo_list = flickr.people_getPublicPhotos(user_id=user_id, extras=extras, per_page=500, page=page ).photos[0]
    flickr_photos = flickr_photo_list.photo
    process_photos(flickr_photos)
    page = page + 1

def process_all_public_favorites_for_user(user_id):
  extras = "license, date_upload, date_taken, owner_name, icon_server, original_format, last_update, geo, tags, machine_tags"
  flickr_photo_list = flickr.favorites_getPublicList(user_id=user_id, extras=extras, per_page=500).photos[0]
  flickr_photos = flickr_photo_list.photo
  process_photos(flickr_photos)

def update():
  # Get the person info
  user_id = settings.FLICKR_USERID

  # Save the flickr person as a Savoy FlickrUser object
  create_or_update_flickr_user(user_id=user_id)

  # Get the photos for this person
  process_all_public_photos_for_user(user_id=user_id)

  # Get the flickr favorites for this person
  process_all_public_favorites_for_user(user_id=user_id)

if __name__ == '__main__':
    update()
