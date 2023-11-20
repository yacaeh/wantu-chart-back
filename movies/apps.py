from django.apps import AppConfig
from app.settings import SCHEDULER_DEFAULT


class MoviesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'movies'

    def ready(self):
        if SCHEDULER_DEFAULT:
            print("REady!?")
            from . import runapscheduler
            runapscheduler.start()