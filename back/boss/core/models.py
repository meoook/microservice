from django.contrib.auth.models import User
from django.db import models
from utils.enums import SocialNetwork, ModuleChoices


class MdBot(models.Model):
    name = models.CharField(max_length=100)
    token = models.CharField(max_length=200)
    social = models.CharField(max_length=2, choices=SocialNetwork.choices)

    def __str__(self):
        return f'{self.social}:{self.name}'


class MdBotChat(models.Model):
    bot = models.ForeignKey(MdBot, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=50)
    chat_id = models.IntegerField()
    public = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.bot} in chat {self.title}'


class MdBotRole(models.Model):
    chat = models.ForeignKey(MdBotChat, on_delete=models.CASCADE)
    role = models.IntegerField(choices=ModuleChoices.choices)

    def __str__(self):
        return f'{self.role.name}'


class MdChatUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    chat = models.ForeignKey(MdBotChat, on_delete=models.CASCADE)
    user_chat_id = models.IntegerField()
    username = models.CharField(max_length=50)
    lang_code = models.CharField(max_length=50, null=True)
    waiting = models.CharField(max_length=50, null=True)  # What kind of message is waiting from this user

    def __str__(self):
        return f'{self.lang_code}:{self.username}'
