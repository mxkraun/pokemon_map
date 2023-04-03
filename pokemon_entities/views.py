import folium
from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from django.utils.timezone import localtime
from .models import *


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def get_absolute_url(request, image_field):
    if image_field:
        return request.build_absolute_uri(image_field.url)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    local_datetime = localtime()
    pokemon_entities = PokemonEntity.objects.filter(appeared_at__lt=local_datetime, disappeared_at__gt=local_datetime)
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            get_absolute_url(request, pokemon_entity.pokemon.image)
        )

    pokemons = Pokemon.objects.all() 
    pokemons_on_page = []
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': get_absolute_url(request, pokemon.image),
            'title_ru': pokemon.title_ru,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    requested_pokemon = get_object_or_404(Pokemon, id=int(pokemon_id))

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    local_datetime = localtime()
    for pokemon_entity in requested_pokemon.entities.filter(appeared_at__lt=local_datetime, disappeared_at__gt=local_datetime):
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            get_absolute_url(request, requested_pokemon.image)
        )

    previous_evolution_pokemon = requested_pokemon.previous_evolution
    previous_evolution = {
        'pokemon_id': previous_evolution_pokemon.id,
        'img_url': get_absolute_url(request, previous_evolution_pokemon.image),
        'title_ru': previous_evolution_pokemon.title_ru,
        'title_en': previous_evolution_pokemon.title_en,
        'title_jp': previous_evolution_pokemon.title_jp,
        'description': previous_evolution_pokemon.description,
    } if previous_evolution_pokemon else None

    next_evolution_pokemon = requested_pokemon.next_evolutions.first()
    next_evolution = {
        'pokemon_id': next_evolution_pokemon.id,
        'img_url': get_absolute_url(request, next_evolution_pokemon.image),
        'title_ru': next_evolution_pokemon.title_ru,
        'title_en': next_evolution_pokemon.title_en,
        'title_jp': next_evolution_pokemon.title_jp,
        'description': next_evolution_pokemon.description,
    } if next_evolution_pokemon else None

    pokemon = {
        'pokemon_id': requested_pokemon.id,
        'img_url': get_absolute_url(request, requested_pokemon.image),
        'title_ru': requested_pokemon.title_ru,
        'title_en': requested_pokemon.title_en,
        'title_jp': requested_pokemon.title_jp,
        'description': requested_pokemon.description,
        'previous_evolution': previous_evolution,
        'next_evolution': next_evolution,      
    }

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon,
    })
