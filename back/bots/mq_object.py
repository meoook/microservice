from utils.mq.objects import MqMessage
from typing import TypedDict


class MqFatherParams(TypedDict, total=False):
    pk: int
    chat_id: int
    token: str
    social: str
    template: str


class MqFatherMessage(MqMessage):
    @property
    def params(self) -> MqFatherParams:
        return self._params
