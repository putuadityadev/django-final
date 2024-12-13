# myprofile/apps.py
from django.apps import AppConfig

class MyprofileConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myprofile'

    def ready(self):
        import myprofile.signals