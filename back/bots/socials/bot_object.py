from abc import ABC, abstractmethod
from utils.enums import SocialName


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
    def message(self, chat_id: int, msg: str) -> None:
        """ Send message in chat """
        ...

    @abstractmethod
    def __handle_msg(self, message: any, *args) -> None:
        """ Handle incoming messages to bot """
        ...
