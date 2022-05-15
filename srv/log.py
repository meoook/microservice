import logging.config

LOGGING = {
    'version': 1,
    # 'disable_existing_loggers': False,
    'formatters': {
        'local': {
            'format': '{asctime} [{levelname:.1}] {name} {module} {message}',
            'style': '{',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'local',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

logging.config.dictConfig(LOGGING)
