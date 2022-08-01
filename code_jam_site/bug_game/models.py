from django.db import models

# Create your models here.


class MapModel(models.Model):
    map = models.JSONField()
    game_id = models.IntegerField()
    game_exists = models.BooleanField(default=False)
