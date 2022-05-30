from utils.mq.objects import MqParams, MqMessage


class MqBotBossParams(MqParams):
    def __init__(self, data: dict):
        self.pk: int = data['pk']
        self.chat_id: int | None = data.get('chat_id')
        self.title: str | None = data.get('title')
        self.public: bool = bool(data.get('public'))
        self.user_id: int | None = data.get('user_id')
        self.username: str | None = data.get('username')
        self.language: str | None = data.get('language')

    def __str__(self):
        return f'BOT:{self.pk} user {self.username} in {"public" if self.public else "private"} chat:{self.chat_id}'

    @property
    def as_dict(self) -> dict[str, str | int]:
        _result: dict[str, str | int] = {'pk': self.pk, 'public': self.public}
        if self.chat_id:
            _result['chat_id'] = self.chat_id
        if self.title:
            _result['title'] = self.title
        if self.user_id:
            _result['user_id'] = self.user_id
        if self.username:
            _result['username'] = self.username
        return _result


class MqBotBossMessage(MqMessage):
    # def __init__(self, source: MqSource, action: MqAction, params: MqParams = None, text: str = None):
    def __init__(self, source: str, action: str, params: dict = None, text: str = None):
        _params = MqBotBossParams(params) if params else None
        super().__init__(source=source, action=action, params=_params, text=text)

    @property
    def params(self) -> MqBotBossParams | None:
        return self._params
