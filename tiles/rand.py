import random
from tiles.models import Tile
from django.db.models import Max
from django.shortcuts import get_object_or_404
from questions.models import Question
import random

def random_questions_try_id_until(queryset, samplesize):
    """ Not Finished """
    max_id = queryset.objects.all().aggregate(max_id=Max("id"))['max_id']
    while True:
        pk = random.randint(1, max_id)
        category = queryset.objects.filter(pk=pk).first()
        if category:
             return category
        
def random_questions_random_sample(queryset, samplesize):
    """ Fastest at this point """
    question_ids = queryset.values_list('id', flat=True)
    try:
        random_ids = random.sample(list(question_ids), samplesize)
    except ValueError:
        return None
    return Question.objects.filter(id__in=random_ids)

def get_random_questions(iterable, samplesize):
    ''' Generates Random Question List based on Tile'''
    results = []
    iterator = iter(iterable)
    # Fill in the first samplesize elements:
    try:
        for _ in range(samplesize):
            results.append(next(iterator))
    except StopIteration:
        raise ValueError("Sample larger than population.")
    random.shuffle(results)  # Randomize their positions
    for i, v in enumerate(iterator, samplesize):
        r = random.randint(0, i)
        if r < samplesize:
            results[r] = v  # at a decreasing rate, replace random items
    return results

def fastest_get_random_questions(queryset, samplesize):
    return random_questions_random_sample(queryset, samplesize)

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
            tile = get_object_or_404(Tile, pk=pk)
            if tile:
                tile_return_list.append(tile)
            else:
                break
        return tile_return_list
