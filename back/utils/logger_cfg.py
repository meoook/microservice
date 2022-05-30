# import logging.config
# logging.config.dictConfig(LOGGING)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'simple': {
            'format': '{asctime} [{levelname:.1}] {message}',
            'style': '{',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'full': {
            'format': '{asctime} [{levelname:.1}] {name} | {message}',
            'style': '{',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'debug': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'full',
        },
    },
    'loggers': {
        'root': {
            'handlers': ['debug'],
            'level': 'DEBUG',
        },
        'bot.father': {
            'handlers': ['debug'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
