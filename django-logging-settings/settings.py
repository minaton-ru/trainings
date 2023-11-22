LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '{asctime} {levelname} {message}'
        'style': '{',  
        },
        'simple_path': {
            'format': '{asctime} {levelname} {pathname} {message}'
        'style': '{',  
        },
        'simple_stack': {
            'format': '{asctime} {levelname} {exc_info} {message}'
        'style': '{',  
        },
        'log': {
            'format': '{asctime} {levelname} {module} {message}'
        'style': '{',  
        },
        'log_stack': {
            'format': '{asctime} {levelname} {message} {pathname} {exc_info}'
        'style': '{',  
        },
        'log_path': {
            'format': '{asctime} {levelname} {message} {pathname}'
        'style': '{',  
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'handlers': {
        'console_debug': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'console_warning': {
            'level': 'WARNING',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple_path'
        },
        'console_error': {
            'level': 'ERROR',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple_stack'
        },
        'file_general': {
            'level': 'INFO',
            'filters': ['require_debug_false'],
            'class': 'logging.FileHandler',
            'filename': 'general.log',
            'formatter': 'log'
        },
        'file_errors': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': 'errors.log',
            'formatter': 'log_stack'
        },
        'file_security': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'security.log',
            'formatter': 'log'
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'log_path'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console_debug', 'console_warning', 'console_error', 'file_general']
        },
        'django.request': {
            'handlers': ['file_errors', 'mail_admins'],
            'propagate': False,
        },
        'django.server': {
            'handlers': ['file_errors', 'mail_admins'],
            'propagate': False,
        },
        'django.template': {
            'handlers': ['file_errors'],
            'propagate': False,
        },
        'django.db_backends': {
            'handlers': ['file_errors'],
            'propagate': False,
        },
        'django.security': {
            'handlers': ['file_security'],
            'propagate': False,
        }
    }
}
