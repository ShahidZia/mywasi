from django import template

from django.db.models import Q

from accounts.models import *
from chat.models import *


ALLOWABLE_VALUES = ("CHAT_WS_SERVER_PROTOCOL", "CHAT_WS_SERVER_HOST", "CHAT_WS_SERVER_PORT")

register = template.Library()


@register.inclusion_tag('chat/partials/conversation.html', takes_context=True)
def render_conversation(context, user, opponent, selected):
    profile = Profile.objects.get(user_id=opponent.id)

    opened = False
    if opponent.username == selected:
        opened = True

    user_1 = user
    user_2 = opponent

    dialog = Dialog.objects.filter(Q(owner=user_1, opponent=user_2) | Q(opponent=user_1, owner=user_2)).last()

    image = None
    if profile.image:
        image = profile.image.url

    context.update({'id': opponent.id, 'userId': opponent.username.split('@')[0].replace('.', ''), 'name': opponent.first_name, 'image': image, 'last': dialog.messages.filter(sender_id=opponent.id).last(), 'opened': opened, 'unread': dialog.messages.filter(read=False, sender=opponent).count})

    return context


@register.inclusion_tag('chat/partials/message.html', takes_context=True)
def render_thread(context, user, msg):

    profile_me = Profile.objects.get(user_id=user.id)

    profile_opponent = Profile.objects.get(user_id=msg.sender.id)

    image_me = None
    image_opponent = None

    if profile_me.image:
        image_me = profile_me.image.url

    if profile_opponent.image:
        image_opponent = profile_opponent.image.url

    context.update({'user': user, 'msg': msg, 'image_me': image_me, 'image_opponent': image_opponent})

    return context


@register.simple_tag
def settings_value(name):
    if name in ALLOWABLE_VALUES:
        return getattr(settings, name, '')
    return ''