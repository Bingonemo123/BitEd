from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import SingleObjectMixin
from django.http import HttpResponseForbidden
from django.utils.translation import gettext as _

from writing.forms import WritingForm

from django.shortcuts import redirect
from django.shortcuts import get_object_or_404


from questions.models import QuestionChoice
from writing.models import UserAnswer
from folder.models import WriteRequestData
from writing.redirects import useranswer_redirect



class WritingFormView(SingleObjectMixin, FormView):
    ''' View for Answered and Answering Question'''
    form_class = WritingForm
    model = UserAnswer
    template_name = 'writing/writing.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['question_object'] = self.object.answer_to
        return  kwargs

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        if "navbar-next-button" in request.POST:
            self.navbar_direction = 'next'
        elif "navbar-previous-button" in request.POST:
            self.navbar_direction = 'previous'

        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        ##################################### Writing View ##########################
        #####################################    Seen +    ##########################
        ##################### Selected + ###########|########### Selected - #########
        ########## Submitted + ###### Submitted - ##|## Submitted + ## Submitted - ##
        ## Correct + ## Correct - ##|               |## Correct - ###|             |
        self.object.answer_state |= 1 # Seen
        if form.cleaned_data['choosen_answer']: # selected
            self.object.answer_state |= 2 # Selected
            self.object.choosen_answer_obj=QuestionChoice.objects.get(
                pk=form.cleaned_data['choosen_answer']
                    )
            
        if not getattr(self, 'navbar_direction', False): # Submitted/Answered
            self.object.answer_state |= 4 # Submitted
            if self.object.wrd.block_mode == 2: # In Training Mode
                if form.cleaned_data.get('choosen_answer') == self.object.answer_to.correct_choice.pk:
                    self.object.answer_state |= 8 # Correct
        self.object.save()
        return  super().form_valid(form)

    def get_success_url(self):
        # when question submitted
        return useranswer_redirect(self.object,
                                    direction=getattr(self, "navbar_direction", None))

# Create your views here.
class QuestionView (LoginRequiredMixin, DetailView):
    '''Writing View - Not Answered Yet'''
    model = UserAnswer
    template_name = 'writing/writing.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(wrd__requested_by=self.request.user)

    def get_context_data(self, **kwargs):
        self.wrd = self.object.wrd
        context =  super().get_context_data(**kwargs)
        context['form'] = WritingForm(self.object.answer_to)
        if self.object.answer_state & 2: # Selected
            context['form'].fields['choosen_answer'].initial = (self.object
                                                .choosen_answer_obj.pk)
        context['wrd'] = self.wrd
        return context
        

class WritingView(View):

    def get(self, request, *args, **kwargs):
        questionview = QuestionView.as_view()
        return questionview(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = WritingFormView.as_view()
        return view(request, *args, **kwargs)

class ReviewingView(DetailView):
    model = UserAnswer
    template_name = 'writing/reviewing.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        writingform = WritingForm(self.object.answer_to)

        if self.object.answer_state & 2: # Selected 
            writingform.fields['choosen_answer'].initial = (self.object
                                                .choosen_answer_obj.pk)

        writingform.fields['choosen_answer'].widget.attrs.update(
                            {"onclick":"return false;"})
        context['form'] = writingform
        context['correct_answer'] = self.object.answer_to.correct_choice.choice_text
        context['next_question_url'] = useranswer_redirect(self.object, direction='next')
        context['previous_question_url'] = useranswer_redirect(self.object, direction='previous')
        return context

def resume_wrd(request, pk):
    resume_wrd = get_object_or_404(WriteRequestData, pk=pk)
    if resume_wrd.finished:
        query = UserAnswer.objects.filter(wrd=resume_wrd).order_by('block_number')
        first_question = query.first()
        return redirect("writing:reviewing", pk=first_question.pk)
    else:
        query = UserAnswer.objects.filter(wrd=resume_wrd, 
                                          choosen_answer_obj=None).order_by('block_number')
        first_question = query.first()
        return redirect("writing:writing", pk=first_question.pk)
