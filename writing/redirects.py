from writing.models import UserAnswer
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse_lazy

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

def useranswer_redirect(current_useranswer, direction=None):

    target_useranswer = get_neighbour(current_useranswer, direction)
    
    if target_useranswer is None: # finished block
        current_useranswer.wrd.finished = True
        current_useranswer.wrd.save()
        return reverse_lazy('home')
            
    else: # submit  and next
        if current_useranswer.wrd.finished:
            return reverse_lazy('writing:reviewing', kwargs={'pk': target_useranswer.pk})
        
        elif current_useranswer.wrd.block_mode == 1: # test mode           
            if direction is None:
                target_useranswer = get_neighbour(current_useranswer, 'next')
            return reverse_lazy('writing:writing', 
                        kwargs={'pk': target_useranswer.pk})
        
        elif target_useranswer.answer_state & 7: # when it training mode question is not answered
            return reverse_lazy('writing:writing', 
                        kwargs={'pk': target_useranswer.pk})
        else:
            return reverse_lazy('writing:reviewing', kwargs={'pk': target_useranswer.pk})
        
       