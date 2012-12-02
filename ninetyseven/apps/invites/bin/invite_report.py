from ninetyseven.apps.invites.models import *

invite_count = Invite.objects.all().count()
invite_sent_count = Invite.objects.exclude(email="").count()
staff_invite_count = Invite.objects.filter(user__is_staff=True).count()
user_invite_count = Invite.objects.filter(user__is_staff=False).count()
staff_invite_sent_count = Invite.objects.filter(user__is_staff=True).exclude(email="").count()
user_invite_sent_count = Invite.objects.filter(user__is_staff=False).exclude(email="").count()

print "Staff invites sent: %s/%s" % (staff_invite_sent_count, staff_invite_count)
print "User invites sent: %s/%s" % (user_invite_sent_count, user_invite_count)
print "Total invites sent: %s/%s" % (invite_sent_count, invite_count)