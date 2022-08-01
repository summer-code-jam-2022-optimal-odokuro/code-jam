from django.apps import AppConfig


class BugGameConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bug_game'

    def ready(self):
        from .models import MapModel
        for map_object in MapModel.objects.all():
            map_object.game_exists = False
            map_object.save()

