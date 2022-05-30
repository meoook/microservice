from enum import Enum
from django.db import models


class SocialNetwork(models.TextChoices):
    TELEGRAM = 'TG'
    INSTAGRAM = 'IN'
    VKONTAKTE = 'VK'
    FACEBOOK = 'FB'
    DISCORD = 'DC'
    SLACK = 'SL'


class ModuleChoices(models.IntegerChoices):
    EMCD = 1
    CURRENCY = 2


class MsgTemplate(Enum):
    HELLO = 'hello'


class MqExchange(Enum):
    BOT = 'bot'


class MqBotRoute(Enum):
    FATHER = 'father'
    BOSS = 'boss'


class MqSource(Enum):
    BOT = 'bot'
    SRV = 'srv'


class MqAction(Enum):
    CREATE = 'create'
    DELETE = 'delete'
    BEAT = 'beat'
    MSG = 'msg'
