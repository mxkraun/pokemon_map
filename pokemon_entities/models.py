from django.db import models


class Pokemon(models.Model):
    title_ru = models.CharField('Название(rus)', max_length=200)
    title_en = models.CharField('Название(eng)', max_length=200, blank=True)
    title_jp = models.CharField('Название(jpn)', max_length=200, blank=True)
    description = models.TextField('Описание', max_length=200, blank=True)
    image = models.ImageField('Картинка', upload_to='images/pokemon', blank=True)
    previous_evolution = models.ForeignKey(
        'self', verbose_name='Из кого эволюционирует', on_delete=models.PROTECT,
        blank=True, null=True, related_name='next_evolutions')

    def __str__(self):
        return f'{self.title_ru}'


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon, verbose_name='Покемон', on_delete=models.PROTECT,
        related_name='pokemon_entities')
    lat = models.FloatField('Широта', blank=True, null=True)
    lon = models.FloatField('Долгота', blank=True, null=True)
    appeared_at = models.DateTimeField('Когда появляется', blank=True, null=True)
    disappeared_at = models.DateTimeField('Когда исчезает', blank=True, null=True)
    level = models.IntegerField('Уровень', blank=True, null=True)
    health = models.IntegerField('Здоровье', blank=True, null=True)
    srength = models.IntegerField('Сила', blank=True, null=True)
    defence = models.IntegerField('Защита', blank=True, null=True)
    stamina = models.IntegerField('Выносливость', blank=True, null=True)
    
    def __str__(self):
        return f'{self.pokemon}: level {self.level}, health {self.health}, strength {self.srength}, defence {self.defence}, stamina {self.stamina }'
