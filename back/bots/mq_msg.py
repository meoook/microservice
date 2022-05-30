from bots.mq_object import MqFatherParams, MqFatherMessage, OtherParams
from utils.enums import SocialNetwork, MqSource, MqAction


class MqFatherMessages:

    def create(self, pk: int, token: str, social: SocialNetwork):
        _params = OtherParams(pk=pk, token=token,social= social.value)
        _msg = MqFatherMessage(source=MqSource.SRV.value, action=MqAction.CREATE.value, params=_params)
        pass

    def delete(self):
        pass

    def msg(self):
        pass

    def beat(self):
        pass
