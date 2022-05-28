import json

from abc import ABC, abstractmethod

from utils.enums import MqSource, MqAction


class MqParams(ABC):
    """ Parameter abstract class for MqMessage """
    @abstractmethod
    def __init__(self, data: dict): ...

    @abstractmethod
    def __str__(self) -> str: ...

    @property
    @abstractmethod
    def as_dict(self) -> dict: ...


class MqMessage:
    """ Base class to serialize rabbitmq messages """

    def __init__(self, source: str, action: str, params: MqParams = None, text: str = None):
        self._source: MqSource = MqSource(source)
        self._action: MqAction = MqAction(action)
        self._params: MqParams | None = params
        self._text: str | None = text

    def __str__(self) -> str:
        _pre_suffix: str = f' params {self._params}' if self._params else ''
        _suffix: str = 'have text' if self._text else 'no text'
        return f'MQ:message from {self._source.name} action {self._action.name}{_pre_suffix} - {_suffix}'

    @classmethod
    def from_bytes(cls, body: bytes):
        _data = json.loads(body)
        return cls(**_data)

    @property
    def as_bytes(self) -> bytes:
        _params = self._params.as_dict if self._params and not isinstance(self._params, dict) else self._params
        _json = {'source': self._source.value, 'action': self._action.value, 'text': self._text, 'params': _params}
        return json.dumps(_json).encode()

    @property
    def source(self) -> MqSource:
        return self._source

    @property
    def action(self) -> MqAction:
        return self._action

    @property
    def params(self) -> MqParams | None:
        return self._params

    @property
    def text(self) -> str | None:
        return self._text
