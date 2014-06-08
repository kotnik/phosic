
from celery.schedules import crontab

CELERYBEAT_SCHEDULE = {
    'every-minute': {
        'task': 'phosic.tasks.calculate_statistics',
        'schedule': crontab(minute='*/30'),
        'args': (1,2),
    },
}
