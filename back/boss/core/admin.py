import logging
from django.contrib import admin, messages

from bots.mq_msg import MqFatherSendMessages
from .models import MdBot, MdBotRole, MdBotChat, MdChatUser

logger = logging.getLogger(__name__)


@admin.register(MdBot)
class MdBotAdmin(admin.ModelAdmin):

    actions = ['make_published']

    @admin.action(description='Mark selected stories as published')
    def make_published(self, request, queryset):
        _selected = queryset.values_list('pk', 'token', 'social')
        # queryset.update(status='p')
        _msg = f'Running {len(_selected)} selected bots'
        logger.info(_msg)
        for _pk, _token, _social in _selected:
            MqFatherSendMessages.create(pk=_pk, token=_token, social=_social)
        self.message_user(request, _msg, messages.SUCCESS)


@admin.register(MdBotRole)
class MdBotRoleAdmin(admin.ModelAdmin):
    pass


@admin.register(MdBotChat)
class MdBotChatAdmin(admin.ModelAdmin):
    pass


@admin.register(MdChatUser)
class MdChatUserAdmin(admin.ModelAdmin):
    pass
