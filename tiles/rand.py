import random
from tiles.models import Tile


def get_random_questions(qs, n):
    ''' Generates Random Question List based on Tile'''
    # avail_ids = list(qs.values_list('id', flat=True))
    while True:
        try:
            pkl = random.sample(qs, n) # change to range
        except ValueError:
            return None
        # tile_return_list = []
        # for pk in pkl:
        #     tile = qs.filter(pk=pk).first()
        #     if tile:
        #         tile_return_list.append(tile)
        #     else:
        #         break
        return pkl

def get_random_home_tiles(n=12):
    ''' Generates Random Tiles List'''
    avail_ids = list(Tile.objects.values_list('id', flat=True))

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
            tile = Tile.objects.filter(pk=pk).first()
            if tile:
                tile_return_list.append(tile)
            else:
                break
        return tile_return_list
