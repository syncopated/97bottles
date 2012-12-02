from ninetyseven.apps.relationships.models import *

class RelationshipManager(models.Manager):
    def relationships_for_user(self, user):
        """
        Relationships for user
        
        Returns a list of friends, people you are following, and followers,
        people that are following you but you are not following.
        """
        # List of users who follow "user".
        followers_users_list = [ relationship.from_user for relationship in self.filter(to_user=user) ]
        
        # List of relationships for users "user" follows, who also follow "user".
        friend_list = self.filter(from_user=user, to_user__in=followers_users_list)
        
        # List of users "user" is friends with.
        friends_users_list = [ relationship.to_user for relationship in friend_list ]
        
        # List of relatiosnhips for users who follow "user", but "user" does not follow back.
        follower_list = self.filter(to_user=user).exclude(from_user__in=friends_users_list)
        
        # List of relationships for users "user" follows, but do not follow "user" back.
        following_list = self.filter(from_user=user).exclude(to_user__in=friends_users_list)

        relationships = {
            'friends': friend_list,
            'followers': follower_list,
            'following': following_list,
        }
        return relationships
    
    def is_following(self, you, them):
        """Answers the question, am I following you?"""
        if self.filter(from_user=you, to_user=them).count() > 0:
            return True
        return False
    
    def is_follower(self, you, them):
        """Answers the question, are you following me?"""
        if self.filter(from_user=them, to_user=you).count() > 0:
            return True
        return False