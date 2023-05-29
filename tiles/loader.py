from django.template.loader import render_to_string
from django.http import JsonResponse

from tiles.rand import get_random_home_tiles

NEWS_COUNT_PER_PAGE = 12

# TODO: Convert To List View 
    
def rnd_tiles_to_context ():
    requested_random_tiles = get_random_home_tiles(n=16)
    if requested_random_tiles is None:
        return {}
    
    for tile in requested_random_tiles:
        tile.get_total_questions_num

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


