from datetime import datetime
from typing import Literal
from dataclasses import dataclass

from src.services.exceptions import SerializeException

CoinName = Literal['bitcoin', 'litecoin', 'bitcoin_cash', 'bitcoin_sv', 'dash', 'eth', 'etc', 'doge']
CoinShortcut = Literal['btc', 'ltc', 'bch', 'btc_sv', 'dash', 'eth', 'etc', 'doge']

_HASHRATE_DELIMITER = 1000000000000


class CoinChoices:
    BITCOIN: CoinName = 'bitcoin'
    LITECOIN: CoinName = 'litecoin'


@dataclass
class Wallet:
    coin: CoinName
    address: str
    balance: float
    total_paid: float
    min_payout: float

    def __str__(self) -> str:
        return f'{self.coin.capitalize()} wallet balance {self.balance} and total payed {self.total_paid}'


class User:
    def __init__(self, name: str):
        self.__name: str = name
        self.__btc_wallet: Wallet | None = None
        self.__ltc_wallet: Wallet | None = None
        self.__wallet_keys: set[str] = {'coin', 'balance', 'total_paid', 'address'}

    def __str__(self) -> str:
        _name = f'User {self.__name}'
        return f'{_name} with {self.__btc_wallet}' if self.__btc_wallet else _name

    @classmethod
    def from_json(cls, data: dict[str, any]) -> any:
        if 'username' not in data:
            return
        _user = cls(data['username'])
        if CoinChoices.BITCOIN in data:
            _user.btc = {'coin': CoinChoices.BITCOIN} | data[CoinChoices.BITCOIN]
        if CoinChoices.LITECOIN in data:
            _user.ltc = {'coin': CoinChoices.LITECOIN} | data[CoinChoices.LITECOIN]
        return _user

    @property
    def btc(self) -> Wallet:
        return self.__btc_wallet

    @btc.setter
    def btc(self, data: dict[str, any]):
        self.__btc_wallet = Wallet(**data) if self.__validate_wallet_data(data) else None

    @property
    def ltc(self) -> Wallet:
        return self.__ltc_wallet

    @ltc.setter
    def ltc(self, data: dict[str, any]):
        self.__ltc_wallet = Wallet(**data) if self.__validate_wallet_data(data) else None

    def __validate_wallet_data(self, data: dict[str, any]) -> bool:
        assert all(_key in data for _key in self.__wallet_keys), SerializeException(f'not a wallet: {data}')
        if all(bool(_item) for _key, _item in data.items() if _key in self.__wallet_keys):
            return True
        return False


@dataclass
class _HsInfo:
    current: int
    hour: int
    day: int

    def __str__(self) -> str:
        return f'Hashrate: current={self.current} hour={self.hour} day={self.day}'

    @classmethod
    def from_json(cls, **kwargs) -> any:
        _kwargs = {}
        for _param_name, _val in kwargs.items():
            match _param_name:
                case 'hashrate':
                    _kwargs['current'] = round(_val / _HASHRATE_DELIMITER)
                case 'hashrate1h':
                    _kwargs['hour'] = round(_val / _HASHRATE_DELIMITER)
                case 'hashrate24h':
                    _kwargs['day'] = round(_val / _HASHRATE_DELIMITER)
        return cls(**_kwargs)


@dataclass
class Worker:
    name: str
    active: bool
    reject: float
    last_beat: datetime
    hashrate: _HsInfo

    def __str__(self) -> str:
        return f'Worker {self.name} ' + f'with {self.hashrate}' if self.active else f'offline since {self.last_beat}'

    @classmethod
    def from_json(cls, **kwargs) -> any:
        _kwargs = {'hashrate': _HsInfo.from_json(**kwargs)}
        for _param_name, _val in kwargs.items():
            match _param_name:
                case 'worker':
                    _kwargs['name'] = _val
                case 'active':
                    _kwargs['active'] = bool(_val)
                case 'reject':
                    _kwargs['reject'] = round(_val * 100)
                case 'lastbeat':
                    _kwargs['last_beat'] = datetime.fromtimestamp(_val)
        return cls(**_kwargs)


@dataclass
class Workers:
    total: int
    online: int
    offline: int
    dead: int
    hashrate: _HsInfo
    list: list[Worker]
    dead_list: dict[str, int] = dict  # {'2201': 1652528382}

    def __str__(self) -> str:
        return f'Workers {self.online} of {self.total} with {self.hashrate}'

    @classmethod
    def from_json(cls, **kwargs) -> any:
        _kwargs = {}
        for _param_name, _val in kwargs.items():
            match _param_name:
                case 'total_count':
                    _kwargs['total'] = _val['all']
                    _kwargs['online'] = _val['active']
                    _kwargs['offline'] = _val['inactive']
                    _kwargs['dead'] = _val.get('dead_count', 0)
                case 'total_hashrate':
                    _kwargs['hashrate'] = _HsInfo.from_json(**_val)
                case 'details':
                    _kwargs['list'] = [Worker.from_json(**_info) for _info in _val]
                case 'detailsDead':
                    _kwargs['dead_list'] = {_k: datetime.fromtimestamp(_v) for _k, _v in _val.items()}
        return cls(**_kwargs)


@dataclass
class Income:
    created: datetime
    amount: float
    hashrate_avg: int

    def __str__(self) -> str:
        return f'Income {self.created.date()} - {self.amount} with hashrate {self.hashrate_avg}'

    @classmethod
    def from_json(cls, **kwargs) -> any:
        _kwargs = {}
        for _param_name, _val in kwargs.items():
            match _param_name:
                case 'timestamp':
                    _kwargs['created'] = datetime.fromtimestamp(int(float(_val)))
                case 'income':
                    _kwargs['amount'] = _val
                case 'total_hashrate':
                    _kwargs['hashrate_avg'] = round(int(_val) / _HASHRATE_DELIMITER)
        return cls(**_kwargs)


@dataclass
class Payout:
    created: datetime
    amount: float
    tx_id: str

    def __str__(self) -> str:
        return f'Payout {self.created.date()} - {self.amount}'

    @classmethod
    def from_json(cls, **kwargs) -> any:
        _kwargs = {}
        for _param_name, _val in kwargs.items():
            match _param_name:
                case 'timestamp':
                    _kwargs['created'] = datetime.fromtimestamp(int(float(_val)))
                case 'amount':
                    _kwargs['amount'] = _val
                case 'txid':
                    _kwargs['tx_id'] = _val
        return cls(**_kwargs)
