from django.template.loader import render_to_string
from django.http import JsonResponse

from django.db.models import F
from django.db.models import Exists
from django.db.models import Subquery, OuterRef
from django.db.models.lookups import Exact

from writing.models import UserAnswer
from questions.models import Question

from tiles.rand import get_random_home_tiles


NEWS_COUNT_PER_PAGE = 12

# TODO: Convert To List View 
    
def rnd_tiles_to_context ():
    ''' Used  in Home Page '''
    requested_random_tiles = get_random_home_tiles(n=1)
    if requested_random_tiles is None:
        return {}
    
    for tile in requested_random_tiles:
        tile.get_total_questions_num

    context = {
                'tiles': requested_random_tiles}
    return context

def get_tiles_view (request):
    ''' Used  in Home Page '''
    context = rnd_tiles_to_context() 
    return render_to_string('tiles/tiles_list_string.html', context, request=request)

def scroll_tiles_load(request, *args, **kwargs):
    ''' Used  in Home Page '''
    context = rnd_tiles_to_context()

    return JsonResponse({
        "scroll_content": render_to_string(
                    'tiles/tiles_list_string.html',
                      context, request=request),
        "end_pagination": False
    }) 


def subquery_personal_filter_stats_loader (q, user):
    mediator = q.annotate(latest_answer_state = Subquery(
                                UserAnswer.objects.filter(answer_to = OuterRef("pk"),
                                wrd__requested_by = user)
                                .order_by("-updated_at")
                                .values("answer_state")[:1]))

    ordered_agr_numbers = [ mediator.filter(
                            latest_answer_state = None).count(), 
                            mediator.filter(
                            latest_answer_state = F('latest_answer_state').bitand(~8)).count(), 
                            mediator.filter(
                            latest_answer_state = F('latest_answer_state').bitand(~2)).count(), 
                            mediator.filter(
                            latest_answer_state = F('latest_answer_state').bitor(8)).count(), 
                            ]
    
    return ordered_agr_numbers

def nested_personal_filter_stats_loader(q, user):
    answers_oi = (UserAnswer.objects.filter(wrd__requested_by=user,
                                                    answer_to__in = q)
                        .order_by("answer_to", "-updated_at")
                        .distinct("answer_to").values('pk'))

    ordered_agr_numbers = [ UserAnswer.objects.filter(
                            answer_state = F('answer_state').bitor(1), # !seens 
                            pk__in= answers_oi).count(),
                            UserAnswer.objects.filter(
                            answer_state = F('answer_state').bitand(~8), 
                            pk__in= answers_oi).count(),
                            UserAnswer.objects.filter(
                            answer_state = F('answer_state').bitand(~2), 
                            pk__in= answers_oi).count(),
                            UserAnswer.objects.filter(
                            answer_state = F('answer_state').bitor(8), 
                            pk__in= answers_oi).count(),
                            ]
    
    return ordered_agr_numbers

def personal_filters_by_questions_with_annotation(choosen_questions, personal_form, user):

    mediator = choosen_questions.annotate(latest_answer_state = Subquery(
                            UserAnswer.objects.filter(answer_to = OuterRef("pk"),
                            wrd__requested_by = user)
                            .order_by("-updated_at")
                            .values("answer_state")[:1]))
        
    questions_queryset = Question.objects.none()
    filtered = False
    if 'unseen' in personal_form.cleaned_data['personal_filter']:
        questions_queryset |= choosen_questions.filter(
                                         ~Exists(Subquery(
                                 UserAnswer.objects.filter(answer_to = OuterRef("pk"),
                                    wrd__requested_by = user))))
        filtered = True
    if 'mistakes' in personal_form.cleaned_data['personal_filter']:
        questions_queryset |= mediator.filter(latest_answer_state = F('latest_answer_state').bitand(~8))
    if 'omitted' in personal_form.cleaned_data['personal_filter']:
        questions_queryset |= mediator.filter(latest_answer_state = F('latest_answer_state').bitand(~2))
    if 'correct' in personal_form.cleaned_data['personal_filter']:
        questions_queryset |= mediator.filter(latest_answer_state = F('latest_answer_state').bitor(8))
    if not filtered:
        questions_queryset = choosen_questions

    return questions_queryset
        

def personal_filters_by_questions(choosen_questions, personal_form, user):
    questions_queryset = Question.objects.none()
    filtered = False
    if 'unseen' in personal_form.cleaned_data['personal_filter']:
        questions_queryset |= choosen_questions.filter(
                                 ~Exists(Subquery(
                                 UserAnswer.objects.filter(answer_to = OuterRef("pk"),
                                                           wrd__requested_by = user))))
        filtered = True
    if 'mistakes' in personal_form.cleaned_data['personal_filter']:
        questions_queryset |= choosen_questions.filter(
                            Exact(Subquery(
                            UserAnswer.objects.filter(answer_to = OuterRef("pk"),
                                                      wrd__requested_by = 1)
                            .order_by("-updated_at")
                            .values("answer_state")[:1])
                            .bitand(8), 0))
        filtered = True
    if 'omitted' in personal_form.cleaned_data['personal_filter']:
        questions_queryset |= choosen_questions.filter(
                            Exact(Subquery(
                            UserAnswer.objects.filter(answer_to = OuterRef("pk"),
                                                      wrd__requested_by = 1)
                            .order_by("-updated_at")
                            .values("answer_state")[:1])
                            .bitand(2), 0))
        filtered = True
    if 'correct' in personal_form.cleaned_data['personal_filter']:
        questions_queryset |= choosen_questions.filter(
                            Exact(Subquery(
                            UserAnswer.objects.filter(answer_to = OuterRef("pk"),
                                                      wrd__requested_by = 1)
                            .order_by("-updated_at")
                            .values("answer_state")[:1])
                            .bitand(8), 8))
        filtered = True
    if not filtered:
        questions_queryset = choosen_questions

    return questions_queryset
