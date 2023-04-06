from django.template.loader import render_to_string
from django.http import JsonResponse

from tiles.rand import get_random_home_tiles

from tiles.models import Tile
from tiles.models import TYPES_OF_TILES
from questions.models import Question
from itertools import chain

NEWS_COUNT_PER_PAGE = 12

# TODO: Convert To List View + Find way for scrolling mechanism

def rnd_tiles_to_context ():
    requested_random_tiles = get_random_home_tiles(n=16)
    if requested_random_tiles is None:
        return {}
    custom_forms = []
    for tile in requested_random_tiles:
        tile_form = {}
        tile_form['img_url'] = tile.img_url
        tile_form['type_of_tile_char'] = dict(TYPES_OF_TILES)[tile.type_of_tile_char]
        tile_form['tile_headline'] = tile.tile_headline
        tile_form['author'] = tile.author
        tile_form['created_at'] = tile.created_at
        tile_form['expected_reward'] = tile.expected_reward
        tile_form['total_pass'] = tile.total_pass
        tile_form['total_writes'] = tile.total_writes
        tile_form['total_questions'] = tile.total_questions
        tile_form['id'] = tile.id
        custom_forms.append(tile_form)
    context = {
                'tiles': custom_forms}
    return context

def get_tiles_view (request, tile_context={}):

    context = rnd_tiles_to_context() 
    context['tile_context'] = tile_context

    return render_to_string('tiles/tiles_list_string.html', context, request=request)

def scroll_tiles_load(request, *args, **kwargs):
    content = ''
    context = rnd_tiles_to_context()
    
    content += render_to_string('tiles/tiles_list_string.html', context, request=request)

    return JsonResponse({
        "scroll_content": content,
        "end_pagination": False
    }) 


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
