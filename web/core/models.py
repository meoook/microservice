from django.db import models


class SocialNetworks(models.TextChoices):
    TELEGRAM = 'TG'
    INSTAGRAM = 'IN'
    VKONTAKTE = 'VK'
    FACEBOOK = 'FB'
    DISCORD = 'DC'
    __empty__ = '--'


class MdBot(models.Model):
    name = models.CharField(max_length=100)
    token = models.CharField(max_length=200)
    social = models.CharField(max_length=2, choices=SocialNetworks)

    def __str__(self):
        return f'{self.social}:{self.name}'


class MdBotChat(models.Model):
    bot = models.ForeignKey(MdBot, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=50)
    chat_id = models.IntegerField()
    public = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.bot} in chat {self.name}'


class MdBotRole(models.Model):
    class ModuleChoices(models.IntegerChoices):
        EMCD = 1
        CURRENCY = 2
        __empty__ = 0

    chat = models.ForeignKey(MdBotChat, on_delete=models.CASCADE)
    role = models.IntegerField(choices=ModuleChoices)

    def __str__(self):
        return f'{self.role.label}'


class MdChatUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    chat = models.ForeignKey(MdBotChat, on_delete=models.CASCADE)
    social_id = models.IntegerField()  # User id in chat
    username = models.CharField(max_length=50)
    lang_code = models.CharField(max_length=50, null=True)
    waiting = models.CharField(max_length=50, null=True)  # What kind of message is waiting from this user

