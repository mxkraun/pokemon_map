from django.db import models
from datetime import datetime


class Pokemon(models.Model):
    image = models.ImageField(upload_to='images/pokemon', blank=True)
    title_ru = models.CharField(max_length=200)
    title_en = models.CharField(max_length=200)
    title_jp = models.CharField(max_length=200)
    description = models.TextField(max_length=200)

    def __str__(self):
        return f'{self.title_ru}'


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.PROTECT, related_name='pokemon_entities')
    lat = models.FloatField()
    lon = models.FloatField()
    appeared_at = models.DateTimeField()
    disappeared_at = models.DateTimeField()
    level = models.IntegerField()
    health = models.IntegerField()
    srength = models.IntegerField()
    defence = models.IntegerField()
    stamina = models.IntegerField()
