import logging
from typing import Callable
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties
from packages.boss_queue.mq_object import MqBotBossMessage
from utils.enums import MqAction, MqExchange, MqBotRoute
from utils.mq.consumer import MqConsumer

logger = logging.getLogger('bot.boss')


class MqBotBossConsumer(MqConsumer):
    """ AMQ Consumer for `boss` server """

    def __init__(self, mq_url: str):
        super().__init__(mq_url, MqExchange.BOT, 'boss', MqBotRoute.BOSS)
        self.__actions: dict[MqAction, Callable[[MqBotBossMessage], None]] = {
            MqAction.BEAT: self.__bot_heartbeat,
            MqAction.MSG: self.__bot_msg,
        }

        try:
            logger.info(f'Start consuming queue "{self.QUEUE}"')
            self._start(self.__callback)
        except Exception as _err:
            logger.warning(f'Stop consuming queue "{self.QUEUE}" - {_err}')

    def __publish_to_father(self, body: bytes) -> None:
        """ Function for bots to put message in queue """
        self._publish(route=MqBotRoute.FATHER, body=body)

    def __callback(self, ch: BlockingChannel, method: Basic.Deliver, _: BasicProperties, body: bytes):
        try:
            _msg: MqBotBossMessage = MqBotBossMessage.from_bytes(body)
        except Exception as _err:
            logger.error(f'Failed to create message from "{body}" - {_err}')
        else:
            self.__do_action(_msg)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def __do_action(self, msg: MqBotBossMessage) -> None:
        try:
            self.__actions[msg.action](msg)
        except Exception as _err:
            logger.error(f'Failed to handle message "{msg}" - {_err}')
