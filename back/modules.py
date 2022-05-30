import os
import sys
import logging.config
from bots.mq_father import BotFatherConsumer
from utils.logger_cfg import LOGGING

logging.config.dictConfig(LOGGING)
logger = logging.getLogger('module.start')


if len(sys.argv) > 1:
    match sys.argv[1]:
        case 'father':
            mq_url: str = os.environ.get('MQ_BROKER_URL', 'amqp://guest:guest@rabbit:5672//')
            logger.info(f'Starting bot.father')
            BotFatherConsumer(mq_url)
        case 'boss_queue':
            logger.info(f'Starting bot.boss')
            pass
        case 'need_django':
            import django
            os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'back.boss.settings')
            django.setup()
        case 'test':
            logger.info('Doing some tests')
        case _:
            logger.warning(f'Module not selected to run')
            exit(1)
