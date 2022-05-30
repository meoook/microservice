from django.contrib import admin
from .models import MdBot, MdBotRole, MdBotChat, MdChatUser


@admin.register(MdBot)
class MdBotAdmin(admin.ModelAdmin):
    pass


@admin.register(MdBotRole)
class MdBotRoleAdmin(admin.ModelAdmin):
    pass


@admin.register(MdBotChat)
class MdBotChatAdmin(admin.ModelAdmin):
    pass


@admin.register(MdChatUser)
class MdChatUserAdmin(admin.ModelAdmin):
    pass
