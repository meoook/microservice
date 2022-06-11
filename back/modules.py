import os
import sys
import logging
from bots.mq_father import BotFatherConsumer

_log_fmt = '{asctime} [{levelname:.1}] {name} | {message}'
logging.basicConfig(format=_log_fmt, datefmt='%Y-%m-%d %H:%M:%S', style='{', level=logging.INFO)
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
