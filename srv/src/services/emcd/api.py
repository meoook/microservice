import logging
from src.services.api_session import AppSession
from .objects import User, Workers, Income, Payout, CoinShortcut

logger = logging.getLogger(__name__)


class EmcdApi:
    __URL = 'https://api.emcd.io/v1'
    __DEFAULT_COIN = 'btc'

    def __init__(self):
        self.__session = AppSession()

    def get_user(self, api_key: str) -> User | None:
        _url: str = f'{self.__URL}/info/{api_key}'
        try:
            _response = self.__session.request(_url)
            return User.from_json(_response)
        except Exception as _err:
            logger.error(f'EMCD: Failed to get user with key `{api_key}` | {_err}')

    def get_workers(self, api_key: str, coin: CoinShortcut = 'btc') -> Workers | None:
        _coin = coin.lower() if coin else self.__DEFAULT_COIN
        _url: str = f'{self.__URL}/{_coin}/workers/{api_key}'
        try:
            _response = self.__session.request(_url)
            return Workers.from_json(**_response)
        except Exception as _err:
            logger.error(f'EMCD: Failed to get workers with key `{api_key}` | {_err}')

    def get_incomes(self, api_key: str, coin: CoinShortcut = 'btc') -> list[Income] | None:
        _coin = coin.lower() if coin else self.__DEFAULT_COIN
        _url: str = f'{self.__URL}/{_coin}/income/{api_key}'
        try:
            _response = self.__session.request(_url)
            return [Income.from_json(**_income) for _income in _response['income']]
        except Exception as _err:
            logger.error(f'EMCD: Failed to get incomes with key `{api_key}` | {_err}')

    def get_payouts(self, api_key: str, coin: CoinShortcut = 'btc') -> list[Payout] | None:
        _coin = coin.lower() if coin else self.__DEFAULT_COIN
        _url: str = f'{self.__URL}/{_coin}/payouts/{api_key}'
        try:
            _response = self.__session.request(_url)
            return [Payout.from_json(**_payout) for _payout in _response['payouts']]
        except Exception as _err:
            logger.error(f'EMCD: Failed to get payouts with key `{api_key}` | {_err}')
