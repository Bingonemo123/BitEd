from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import SingleObjectMixin
from django.http import HttpResponseForbidden
from django.utils.translation import gettext as _
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse

from django.shortcuts import redirect
from django.shortcuts import get_object_or_404


from questions.models import QuestionChoice
from writing.models import UserAnswer
from tiles.models import WriteRequestData
from writing.redirects import useranswer_redirect

# Forms
# https://stackoverflow.com/questions/27321692/override-a-django-generic-class-based-view-widget
class WritingForm(forms.ModelForm):
    
    choosen_answer = forms.ChoiceField( widget=forms.RadioSelect(),
                                       label='Choose answer',
                                       required=False)

    def __init__(self, question_object, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.choices_query = QuestionChoice.objects.filter(
                choice_to=question_object).order_by("?")
        
        #FIXME: Remove "lowest pk is correct" bug
        # Or remove pk from radio or random save correct answer

        self.RADIOCHOICES = [
            (obj.pk, obj.choice_text) 
            for obj in self.choices_query
        ]

        self.fields['choosen_answer'].choices = self.RADIOCHOICES

    class Meta:
        model = UserAnswer
        fields = ['choosen_answer']

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

        if form.cleaned_data['choosen_answer']:
            if (getattr(self, 'navbar_direction', None)
                    and  self.object.answer_state & 9):
                self.object.answer_state = 4 # selected
            else:
                self.object.answer_state = 8 # answered
            self.object.choosen_answer_obj=QuestionChoice.objects.get(
                pk=form.cleaned_data['choosen_answer']
                )
            self.object.save()
        else:
            self.object.anwser_state = 2 # seen
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
        if self.object.answer_state & 12: # selected or answered
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

        if self.object.answer_state & 12: # selected or answered
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
