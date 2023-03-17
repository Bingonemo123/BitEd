from django.template.loader import render_to_string
from tiles.models import TYPES_OF_TILES
from django.http import JsonResponse

from tiles.rand import get_random_home_tiles

NEWS_COUNT_PER_PAGE = 12

# TODO: Convert To List View + Find way for scrolling mechanism
def rnd_tiles_to_context ():
    requested_random_tiles = get_random_home_tiles(n=16)
    if requested_random_tiles is None:
        return {}
    custom_forms = []
    for hpt in requested_random_tiles:
        tile_form = {}
        tile_form['img_url'] = hpt.img_url
        tile_form['type_of_tile_char'] = dict(TYPES_OF_TILES)[hpt.type_of_tile_char]
        tile_form['tile_headline'] = hpt.tile_headline
        tile_form['author'] = hpt.author
        tile_form['tiles'] = hpt.children.all()
        tile_form['created_at'] = hpt.created_at
        tile_form['expected_reward'] = hpt.expected_reward
        tile_form['total_pass'] = hpt.total_pass
        tile_form['total_writes'] = hpt.total_writes
        tile_form['total_questions'] = hpt.total_questions
        tile_form['id'] = hpt.id
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
