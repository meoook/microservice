from enum import Enum


class SocialName(Enum):
    TELEGRAM = 'TG'
    INSTAGRAM = 'IN'
    VKONTAKTE = 'VK'
    FACEBOOK = 'FB'
    DISCORD = 'DC'
    SLACK = 'SL'


class MsgTemplate(Enum):
    HELLO: str = 'hello'


class MqExchange(Enum):
    BOT = 'bot'


class MqBotRoute(Enum):
    FATHER = 'father'
    BOSS = 'boss'


class MqSource(Enum):
    BOT: str = 'bot'
    SRV: str = 'srv'


class MqAction(Enum):
    CREATE: str = 'create'
    DELETE: str = 'delete'
    BEAT: str = 'beat'
    MSG: str = 'msg'
