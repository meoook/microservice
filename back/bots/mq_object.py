from utils.enums import SocialName, MsgTemplate
from utils.mq.objects import MqParams, MqMessage


class MqFatherParams(MqParams):
    def __init__(self, data: dict):
        _social: str = data.get('social')
        _template: str = data.get('template')
        self.pk: int | None = data.get('pk')
        self.chat_id: int | None = data.get('chat_id')
        self.token: str | None = data.get('token')
        self.social: SocialName | None = SocialName(_social) if _social else None
        self.template: MsgTemplate | None = MsgTemplate(_template) if _template else None

    def __str__(self) -> str:
        if self.social:
            _name: str = self.social.value
            _name += f':{self.pk}' if self.pk else ''
        else:
            _name: str = f'PK:{self.pk}' if self.pk else ''
        _name += '|' if _name and self.chat_id else ''
        _name += f'CHAT:{self.chat_id}' if self.chat_id else ''
        _name += '|' if _name and self.template else ''
        _name += f'TMP:{self.template.name}' if self.template else ''
        return _name

    @property
    def as_dict(self) -> dict[str, str | int]:
        _result: dict[str, str | int] = {'social': self.social.value} if self.social else {}
        if self.pk:
            _result['pk'] = self.pk
        if self.token:
            _result['token'] = self.token
        if self.template:
            _result['template'] = self.template.value
        return _result


class MqFatherMessage(MqMessage):
    def __init__(self, source: str, action: str, params: dict = None, text: str = None):
        _params = MqFatherParams(params) if params else None
        super().__init__(source=source, action=action, params=_params, text=text)

    @property
    def params(self) -> MqFatherParams | None:
        return self._params


class MqBotSource:
    __DATA_KEYS: list = ['bot_id', 'chat_id', 'name', 'public']

    def __init__(self, data: dict):
        assert all(_val in data for _val in self.__DATA_KEYS), f'wrong parameters: {[*data.keys()]}'
        assert data['social'] in SocialName, f'wrong social "{data["social"]}"'
        self.bot_id: int = data['bot_id']
        self.chat_id: int = data['chat_id']
        self.name: str = data['name']
        self.public: bool = data['public']

    def __repr__(self) -> dict:
        return {'bot_id': self.bot_id, 'chat_id': self.chat_id, 'name': self.name, 'public': self.public}

    def __str__(self):
        return f'{self.bot_id}:{self.chat_id}:{"public" if self.public else "private"}'
