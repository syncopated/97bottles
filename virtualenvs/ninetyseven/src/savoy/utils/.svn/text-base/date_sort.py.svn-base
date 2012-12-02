from django.template.defaultfilters import dictsort,dictsortreversed

def sort_items_by_date(object_list, date_fields="date_published, timestamp, pub_date, date_submitted, date_created", recent_first=False):
  """
  Given a list of heterogeneous items (instances from several different models) and a list of
  possible date field names, sort the items by date. Any items in the list without a date field
  attribute will be left out of the results. Defaults to most recent items last, but accepts a
  recent_first argument to reverse the chronology.
  """
  date_field_list = date_fields.split(",")
  object_dict_list = []
  for object in object_list:
    if object:
      object_date_field = None
      for field in date_field_list:
        for f in object._meta.fields:
          if f.name == field:
            object_date_field = f.name
            break
        if object_date_field:
          object_dict = { 'date': getattr(object, object_date_field), 'object': object }
          object_dict_list.append(object_dict)
  
  if recent_first:
    sorted_item_dicts = dictsortreversed(object_dict_list, 'date')
  else:
    sorted_item_dicts = dictsort(object_dict_list, 'date')
  sorted_items = []
  for item in sorted_item_dicts:
    if item['object'] not in sorted_items:
      sorted_items.append(item['object'])
  return sorted_items