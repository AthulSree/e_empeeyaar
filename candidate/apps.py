from django.apps import AppConfig  # type: ignore


class CandidateConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'candidate'
