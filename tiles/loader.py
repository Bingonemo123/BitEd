from django.template.loader import render_to_string
from django.http import JsonResponse
from django.core.cache import cache

from tiles.rand import get_random_home_tiles

from tiles.models import Tile
from itertools import chain

NEWS_COUNT_PER_PAGE = 12

# TODO: Convert To List View 

def get_all_questions(tile):
    questions_queryset = tile.questions.all()
    for subtile in Tile.objects.filter(parent=tile):
        questions_queryset = chain(questions_queryset, get_all_questions(subtile))

    return questions_queryset


def get_all_questions_num(tile):
    questions_num = tile.questions.all().count()
    for subtile in Tile.objects.filter(parent=tile):
        questions_num += get_all_questions_num(subtile)

    return questions_num


def rnd_tiles_to_context ():
    requested_random_tiles = get_random_home_tiles(n=16)
    if requested_random_tiles is None:
        return {}
    
    for tile in requested_random_tiles:
        tile_total = cache.get(str(tile.pk))
        if tile_total is None:
            tile_total = get_all_questions_num(tile)
            cache.add(str(tile.pk), tile_total)
            tile.total_questions = tile_total
            tile.save()

    context = {
                'tiles': requested_random_tiles}
    return context

def get_tiles_view (request):
    context = rnd_tiles_to_context() 
    return render_to_string('tiles/tiles_list_string.html', context, request=request)

def scroll_tiles_load(request, *args, **kwargs):
    context = rnd_tiles_to_context()

    return JsonResponse({
        "scroll_content": render_to_string(
                    'tiles/tiles_list_string.html',
                      context, request=request),
        "end_pagination": False
    }) 


