from typing import Callable
from abc import ABC, abstractmethod
from utils.enums import SocialNetwork


class SocialBot(ABC):
    @abstractmethod
    def __init__(self, pk: int, token: str, publish: Callable[[bytes], None]): ...

    @property
    @abstractmethod
    def pk(self) -> int:
        """ Return database pk value """
        ...

    @property
    @abstractmethod
    def social(self) -> SocialNetwork:
        """ Return two-letters for bot social network """
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
    def message(self, chat_id: int, msg: str, template: str = None) -> None:
        """ Send message in chat """
        ...

    @abstractmethod
    def _handle_msg(self, message: any, *args) -> None:
        """ Handle incoming messages to bot """
        ...

    @abstractmethod
    def _publish(self, body: bytes) -> None:
        """ Mq publish message """
        ...
