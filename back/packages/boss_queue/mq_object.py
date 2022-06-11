from typing import TypedDict

from utils.mq.objects import MqMessage


class MqBotBossParams(TypedDict, total=False):
    pk: int
    chat_id: int
    title: str
    public: bool
    user_id: int
    username: str
    language: str


class MqBotBossMessage(MqMessage):
    @property
    def params(self) -> MqBotBossParams | None:
        return self._params
