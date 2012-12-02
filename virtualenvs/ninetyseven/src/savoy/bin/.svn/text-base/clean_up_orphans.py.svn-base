from django.conf import settings
from savoy.core.geo.models import GeolocatedItem
from tagging.models import TaggedItem
from savoy.contrib.comments.models import Comment
from savoy.contrib.aggregator.models import ContentItem

# First, remove any Comment objects that don't have an associated content object.
# This happens when content objects get deleted, but their associated Comment objects don't.
orphans = Comment.orphaned_comments.all()
orphan_deleted_count = 0
for item in orphans:
  item.delete()
  orphan_deleted_count = orphan_deleted_count + 1
print "Deleted " + str(orphan_deleted_count) + " orphaned Comment objects."
    
# Finally, remove any TaggedItem object that don't have an associated content object.
# This happens when content objects get deleted, but their associated TaggedItem object doesn't.
orphans = []
orphan_deleted_count = 0
for item in TaggedItem.objects.all():
    if item.object == None:
        orphans.append(item)
        item.delete()
        orphan_deleted_count = orphan_deleted_count + 1
print "Deleted " + str(orphan_deleted_count) + " orphaned TaggedItem objects."