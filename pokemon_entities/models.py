from django.db import models
from datetime import datetime


class Pokemon(models.Model):
    title_ru = models.CharField('Название(rus)', max_length=200)
    title_en = models.CharField('Название(eng)', max_length=200)
    title_jp = models.CharField('Название(jpn)', max_length=200)
    description = models.TextField('Описание', max_length=200)
    image = models.ImageField('Картинка', upload_to='images/pokemon')
    previous_evolution = models.ForeignKey(
        'self', verbose_name='Из кого эволюционирует',
        on_delete=models.PROTECT, blank=True, null=True,
        related_name='next_evolutions'
    )

    def __str__(self):
        return f'{self.title_ru}'


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, verbose_name='Покемон', on_delete=models.PROTECT, related_name='pokemon_entities')
    lat = models.FloatField('Широта')
    lon = models.FloatField('Долгота')
    appeared_at = models.DateTimeField('Когда появляется')
    disappeared_at = models.DateTimeField('Когда исчезает')
    level = models.IntegerField('Уровень')
    health = models.IntegerField('Здоровье')
    srength = models.IntegerField('Сила')
    defence = models.IntegerField('Защита')
    stamina = models.IntegerField('Выносливость')
    
    def __str__(self):
        return f'{self.pokemon}: lvl {self.level}, hp {self.health}'
