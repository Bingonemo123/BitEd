import random
from tiles.models import Tile
from django.shortcuts import get_object_or_404
from questions.models import Question
from django.core.cache import cache
import random
 
first_in_pair = [4773, 4777, 4779, 4781, 4791, 4793, 4797, 4808, 4810, 4817,
                 4913, 4931, 4936, 4938, 6996, 7686, 7690, 7708, 9566, 10145, 
                 10660, 11948, 12037, 12111, 12114, 12135, 12417, 12673, 12684,
                 18658, 20678, 20724, 20786, 20886, 21248, 21323, 21361, 22326,
                 106048, 106289, 106664, 106764, 107151, 107273, 107754, 107776]
second_in_pair = [4774, 4778, 4780, 4782, 4792, 4794, 4798, 4809, 4811, 4818,
                  4914, 4932, 4937, 4939, 6981, 7687, 7691, 7709, 9563, 10146, 
                  10661, 11947, 12038, 12112, 12115, 12136, 12418, 12674, 12685, 
                  18659, 20679, 20725, 20787, 20887, 21249, 21324, 21362, 22327, 
                  106049, 106290, 106665, 106765, 107152, 107274, 107755, 107777]

def random_questions_random_sample(queryset, samplesize):
    """ Fastest at this point """
    question_ids = queryset.values_list('id', flat=True)
    try:
        random_ids = random.sample(list(question_ids), samplesize)
    except ValueError:
        return None
    
    first_in_pair = cache.get("Paired_questions_first_in_pair")
    second_in_pair = cache.get("Paired_questions_second_in_pair")
    if first_in_pair is None or second_in_pair is None:
        bundle_of_questions = Question.objects.filter(next_question_in_group__isnull=False).values_list(('id', 'next_question_in_group'))
        first_in_pair = []
        second_in_pair = []
        for x , y in bundle_of_questions:
            first_in_pair.append(x)
            second_in_pair.append(y)
        cache.add("Paired_questions_first_in_pair", first_in_pair, timeout=28800)
        cache.add("Paired_questions_second_in_pair", second_in_pair, timeout=None)
    
    binded_qid = []
    for qid in random_ids:
        if qid in first_in_pair:
            binded_qid.append(qid)
            binded_qid.append(second_in_pair[first_in_pair.index(qid)])
        elif qid in second_in_pair:
            binded_qid.append(first_in_pair[second_in_pair.index(qid)])
            binded_qid.append(qid)
        else:
            binded_qid.append(qid)

    return Question.objects.filter(id__in=binded_qid)


def fastest_get_random_questions(queryset, samplesize):
    return random_questions_random_sample(queryset, samplesize)
 
# tiles  

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

# def random_questions_try_id_until(queryset, samplesize):
#     """ Not Finished """
#     max_id = queryset.objects.all().aggregate(max_id=Max("id"))['max_id']
#     while True:
#         pk = random.randint(1, max_id)
#         category = queryset.objects.filter(pk=pk).first()
#         if category:
#              return category


# def get_random_questions(iterable, samplesize):
#     ''' Generates Random Question List based on Tile'''
#     results = []
#     iterator = iter(iterable)
#     # Fill in the first samplesize elements:
#     try:
#         for _ in range(samplesize):
#             results.append(next(iterator))
#     except StopIteration:
#         raise ValueError("Sample larger than population.")
#     random.shuffle(results)  # Randomize their positions
#     for i, v in enumerate(iterator, samplesize):
#         r = random.randint(0, i)
#         if r < samplesize:
#             results[r] = v  # at a decreasing rate, replace random items
#     return results
