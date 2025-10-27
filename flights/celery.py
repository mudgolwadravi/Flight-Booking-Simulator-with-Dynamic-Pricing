from celery import Celery

app = Celery('project_name')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'update-market-every-5-min': {
        'task': 'flights.tasks.update_flight_market',
        'schedule': 300,  # 5 minutes
    },
}
