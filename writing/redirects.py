""" User Redirects Functions used in Views"""
from django.urls import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist

from django.db.models import F, Case, When
from django.db.models import Subquery, OuterRef
from django.db.models.lookups import Exact

from writing.models import UserAnswer
from questions.models import Question

def get_neighbour(useranswer, direction=None):
    if direction == 'previous':
        if useranswer.block_number == 1:
            previous_question = useranswer
        else:
            block_questions = UserAnswer.objects.filter(wrd=useranswer.wrd)
            previous_question = block_questions.get(
                block_number = useranswer.block_number - 1
                )
        return previous_question
    elif direction == 'next' :
        block_questions = UserAnswer.objects.filter(wrd=useranswer.wrd)
        try:
            next_question = block_questions.get(
                block_number = useranswer.block_number + 1
                )
        except ObjectDoesNotExist:
            return None
        return next_question
    else:
        return useranswer

def finish_wrd(current_useranswer):
    current_useranswer.wrd.finished = True
    current_useranswer.wrd.save()
    # update answer state in db
    current_useranswer.wrd.useranswer_set.all().update( 
        answer_state= Case (
        When(
        Exact(
        Subquery(
        Question.objects.filter(
        pk=OuterRef("answer_to")).values("correct_choice")[:1]),
        F("choosen_answer_obj")), then=F('answer_state').bitor(8)), 
        default=F('answer_state').bitand(~8)))
    return reverse_lazy('home')

def useranswer_redirect(current_useranswer, direction=None):

    target_useranswer = get_neighbour(current_useranswer, direction)

    if target_useranswer is None: # finish block Training
        return finish_wrd(current_useranswer)
    else: # submit  and next
        if current_useranswer.wrd.finished:
            return reverse_lazy('writing:reviewing', kwargs={'pk': target_useranswer.pk})
        elif current_useranswer.wrd.block_mode == 1: # test mode
            if direction is None:
                target_useranswer = get_neighbour(current_useranswer, 'next')
                if target_useranswer is None: # finish block Test
                    return finish_wrd(current_useranswer)
            return reverse_lazy('writing:writing',
                        kwargs={'pk': target_useranswer.pk})
        elif not target_useranswer.answer_state & 4: 
            # Training mode, question is not answered/submitted
            return reverse_lazy('writing:writing',
                        kwargs={'pk': target_useranswer.pk})
        else:
            return reverse_lazy('writing:reviewing', kwargs={'pk': target_useranswer.pk})
    