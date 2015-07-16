"""
This script registers the models with the Moderation app
"""
from moderation import moderation
from moderation.moderator import GenericModerator
from .models import *

class Moderator(GenericModerator):
    fields_exclude=['updated','hits']
    visible_until_rejected=True
    auto_approve_for_groups=['*']


    def is_auto_approve(self, obj, user):
        if obj.state == "raw":
            return self.reason('Not Submitted Yet !')
        super(Moderator, self).is_auto_approve(obj, user)

moderation.register(Tutorial,Moderator)
moderation.register(Snippet,Moderator)
moderation.register(Wiki,Moderator)
moderation.register(Blog,Moderator)
moderation.register(Announcement,Moderator)
moderation.register(News,Moderator)
moderation.register(Package,Moderator)
moderation.register(Event,Moderator)
moderation.register(EducationalResource,Moderator)