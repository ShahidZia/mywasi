from django import template
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db.models import Q

from accounts.models import *
from django_private_chat.models import *

register = template.Library()

@register.inclusion_tag('django_private_chat/partials/conversation.html',takes_context=True)
def render_conversation(context, user ,opponent):
    profile = Profile.objects.get(user_id= opponent.id)

    user_1 = user
    user_2 = opponent



    dialog = Dialog.objects.filter(Q(owner=user_1, opponent=user_2) | Q(opponent=user_1, owner=user_2)).last()

    image = 'https://www.communitylandtrust.ca/wp-content/uploads/2015/10/placeholder.png'
    if profile.image:
        image = profile.image.url

    context.update({'id':opponent.id, 'userId': opponent.username.split('@')[0].replace('.',''), 'name': opponent.first_name, 'image' : image , 'last': dialog.messages.last() })

    return context

@register.inclusion_tag('django_private_chat/partials/thread.html',takes_context=True)
def render_thread(context, user ,msg):

    profile = Profile.objects.get(user_id= user.id)

    image = 'https://www.communitylandtrust.ca/wp-content/uploads/2015/10/placeholder.png'

    if profile.image:
        image = profile.image.url

    context.update({'user':user, 'msg': msg, 'image' : image })

    return context

