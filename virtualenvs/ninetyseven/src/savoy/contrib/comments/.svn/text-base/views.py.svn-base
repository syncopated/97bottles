import datetime

from django.shortcuts import render_to_response
from django.http import Http404
from django.views.generic import list_detail
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType
from django.template import RequestContext
from django.core.mail import send_mail
from django.utils.encoding import smart_unicode

from savoy.contrib.comments.models import Comment
from savoy.contrib.comments.forms import CommentForm

def post_comment(request):
  if not request.POST:
    raise Http404, "Only POSTs are allowed"
  content_type = ContentType.objects.get(pk=int(request.POST['target_content_type']))
  try:
    obj = content_type.get_object_for_this_type(pk=int(request.POST['target_object_id']))
  except ObjectDoesNotExist:
    raise Http404, "The comment form had an invalid 'target' parameter -- the object ID was invalid"
  new_comment = request.POST.copy()
  new_comment['object_id'] = obj.id
  new_comment['content_type'] = content_type.id
  new_comment['date_submitted'] = datetime.datetime.now()
  new_comment['author_ip_address'] = request.META.get('REMOTE_ADDR', '')
  form = CommentForm(new_comment)
  if form.is_valid():
    if not request.POST.has_key('preview'):
      new_comment = form.save()
      comment_parent_object = new_comment.parent_object()
      context = { 
        'comment': new_comment,
        'object_commented_on': comment_parent_object,
      }
      return render_to_response('comments/comment_posted.html',context, context_instance=RequestContext(request))
    else:
      context = {
        'preview': True,
        'comment': new_comment,
        'comment_target_content_type': content_type.id,
        'comment_target_object_id': obj.id,
        'comment_form': form,
      }
      return render_to_response('comments/comment_preview.html', context, context_instance=RequestContext(request))
  else:
    context = {
      'preview': True,
      'errors': True,
      'comment_target_content_type': content_type.id,
      'comment_target_object_id': obj.id,
      'comment_form': form,
    }
    return render_to_response('comments/comment_preview.html', context, context_instance=RequestContext(request))
