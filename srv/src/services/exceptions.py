class SerializeException(Exception):
    def __init__(self, message):
        super().__init__(f'serialize error - {message}')
