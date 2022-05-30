import json
from utils.enums import MqSource, MqAction


class MqMessage:
    """ Base class to serialize rabbitmq messages """

    def __init__(self, source: str, action: str, params: dict = None, text: str = None):
        self._source: MqSource = MqSource(source)
        self._action: MqAction = MqAction(action)
        self._params: dict | None = params
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
        _json = {'source': self._source.value, 'action': self._action.value, 'text': self._text, 'params': self._params}
        return json.dumps(_json).encode()

    @property
    def source(self) -> MqSource:
        return self._source

    @property
    def action(self) -> MqAction:
        return self._action

    @property
    def params(self) -> dict | None:
        return self._params

    @property
    def text(self) -> str | None:
        return self._text
