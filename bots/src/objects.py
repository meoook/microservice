import json
from typing import Literal
from abc import ABC, abstractmethod

FatherAction = Literal['create', 'delete', 'beat', 'msg']
FatherActions: tuple[str, ...] = ('create', 'delete', 'beat', 'msg')

SocialName = Literal['TG', 'IN', 'VK', 'FB', 'DC']


class SocialNames:
    TG: SocialName = 'TG'
    IN: SocialName = 'IN'
    VK: SocialName = 'VK'
    FB: SocialName = 'FB'
    DC: SocialName = 'DC'

    @property
    def list(self) -> tuple[SocialName, ...]:
        return 'TG', 'IN', 'VK', 'FB', 'DC'


class SocialBot(ABC):

    @abstractmethod
    def __init__(self, pk: int, token: str): ...

    @property
    @abstractmethod
    def pk(self) -> int:
        """ Return database pk value """
        ...

    @property
    @abstractmethod
    def social(self) -> SocialName:
        """ Return tow-letters for bot social network """
        ...

    @abstractmethod
    def start(self) -> None:
        """ Start bot listening """
        ...

    @abstractmethod
    def stop(self) -> None:
        """ Stop bot poling """
        ...

    @abstractmethod
    def beat(self) -> None:
        """ Check bot life status """
        ...

    @abstractmethod
    def message(self, chat_id: int, msg: str) -> None:
        """ Send message in chat """
        ...

    @abstractmethod
    def __handle_msg(self, message: any, *args) -> None:
        """ Handle incoming messages to bot """
        ...


class BotFatherMessage:
    """ Command to BotFather """
    __DATA_KEYS: list = ['pk', 'social', 'action']

    def __init__(self, data: dict):
        assert all(_val in data for _val in self.__DATA_KEYS), f'wrong parameters: {[*data.keys()]}'
        assert data['action'] in FatherActions, f'wrong action "{data["action"]}"'
        assert data['social'] in SocialNames.list, f'wrong social "{data["social"]}"'
        self.pk: int = data['pk']
        self.social: SocialName = data['social']
        self.action: FatherAction = data['action']
        self.message: any = data['message'] if 'message' in data else None

    @classmethod
    def from_bytes(cls, body: bytes):
        _data = json.loads(body)
        return cls(_data)

    @property
    def as_bytes(self) -> bytes:
        _json = {'pk': self.pk, 'social': self.social, 'action': self.action}
        if self.message:
            _json['message'] = self.message
        return json.dumps(_json).encode()

    def __str__(self) -> str:
        return f'{self.social}:{self.pk} {self.action}'


EventType = Literal['bot.msg', 'bot.cmd', 'srv.action']


class AmpqBotSource:
    __DATA_KEYS: list = ['bot_id', 'chat_id', 'name', 'public']

    def __init__(self, data: dict):
        assert all(_val in data for _val in self.__DATA_KEYS), f'wrong parameters: {[*data.keys()]}'
        assert data['social'] in SocialNames.list, f'wrong social "{data["social"]}"'
        self.bot_id: int = data['bot_id']
        self.chat_id: int = data['chat_id']
        self.name: str = data['name']
        self.public: bool = data['public']

    def __repr__(self) -> dict:
        return {'bot_id': self.bot_id, 'chat_id': self.chat_id, 'name': self.name, 'public': self.public}

    def __str__(self):
        return f'{self.bot_id}:{self.chat_id}:{"public" if self.public else "private"}'


class AmqpMessage:
    """ Class to manage rabbitmq messages (serialize and validate) """
    __DATA_KEYS: list = ['event', 'source']
    source: AmpqBotSource

    def __init__(self, data: dict):
        assert all(_val in data for _val in self.__DATA_KEYS), f'wrong parameters: {[*data.keys()]}'
        self.event: EventType = data['event']
        if self.event == 'bot':
            self.source: AmpqBotSource = AmpqBotSource(data['source'])
        else:
            raise AssertionError(f'invalid event type `{self.event}` for amqp-message')
        self.user: any = data['user'] if 'user' in data else None
        self.message: any = data['message'] if 'message' in data else None

    @classmethod
    def from_bytes(cls, body: bytes):
        _data = json.loads(body)
        return cls(_data)

    @property
    def as_bytes(self) -> bytes:
        _json = {'event': self.event, 'source': self.source}
        if self.user:
            _json['user'] = self.user
        if self.message:
            _json['message'] = self.message
        return json.dumps(_json).encode()

    def __str__(self) -> str:
        return f'amqp:{self.event}:{self.source}'
