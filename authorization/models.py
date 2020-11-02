from django.db import models

class User(models.Model):
    open_id = models.CharField(max_length=32, unique=True)
    nickname = models.CharField(max_length=255)
    focus_cities = models.TextField(default='[]')
    focus_constellations = models.TextField(default='[]')
