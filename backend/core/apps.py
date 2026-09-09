from django.apps import AppConfig
from django.db.models.signals import post_migrate


def auto_seed_on_migrate(sender, **kwargs):
    if sender.name == 'core':
        try:
            from departments.models import Department
            if Department.objects.count() == 0:
                from django.core.management import call_command
                call_command('seed_data')
        except Exception:
            pass


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        post_migrate.connect(auto_seed_on_migrate, sender=self)
