from bots.mq_object import MqFatherParams, MqFatherMessage
from utils.enums import MqSource, MqAction, MqBotRoute
from utils.mq.publish import MqPublish


class MqFatherSendMessages:
    # TODO - set source in init and publish ?

    @staticmethod
    def create(pk: int, token: str, social: str) -> None:
        _params = MqFatherParams(pk=pk, token=token, social=social)
        _msg = MqFatherMessage(source=MqSource.SRV.value, action=MqAction.CREATE.value, params=_params)
        _publisher = MqPublish()
        _publisher.publish(MqBotRoute.FATHER, _msg.as_bytes)

    @staticmethod
    def delete(pk: int) -> None:
        _params = MqFatherParams(pk=pk)
        _msg = MqFatherMessage(source=MqSource.SRV.value, action=MqAction.DELETE.value, params=_params)
        _publisher = MqPublish()
        _publisher.publish(MqBotRoute.FATHER, _msg.as_bytes)

    @staticmethod
    def msg(pk: int, text: str, template: str = None) -> None:
        _params = MqFatherParams(pk=pk, template=template) if template else MqFatherParams(pk=pk)
        _msg = MqFatherMessage(source=MqSource.SRV.value, action=MqAction.MSG.value, params=_params, text=text)
        _publisher = MqPublish()
        _publisher.publish(MqBotRoute.FATHER, _msg.as_bytes)

    @staticmethod
    def beat() -> None:
        _msg = MqFatherMessage(source=MqSource.SRV.value, action=MqAction.BEAT.value)
        _publisher = MqPublish()
        _publisher.publish(MqBotRoute.FATHER, _msg.as_bytes)
