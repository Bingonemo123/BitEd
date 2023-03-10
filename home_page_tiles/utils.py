import random
from .models import HomePageTile
# from django.db.models import Max

'''ToDo resequesnce Tables and use Max id and range'''

def get_random_home_tiles(n=12):
    avail_ids = list(HomePageTile.objects.values_list('id', flat=True))
    # max_id = HomePageTile.objects.all().aggregate(max_id=Max('id'))['max_id']

    while True:
        try:
            pkl = random.sample(avail_ids, n) 
        except ValueError:
            try:
                return get_random_home_tiles(n=len(avail_ids))
            except ValueError:
                return []
        tile_return_list = []
        for pk in pkl:
            tile = HomePageTile.objects.filter(pk=pk).first()
            if tile:
                tile_return_list.append(tile)
            else:
                break
        return tile_return_list
