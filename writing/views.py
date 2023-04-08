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

# Forms
# https://stackoverflow.com/questions/27321692/override-a-django-generic-class-based-view-widget
class WritingForm(forms.ModelForm):
    
    choosen_answer = forms.ChoiceField( widget=forms.RadioSelect(),
                                       label='Choose answer')

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
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        result =  super().form_valid(form)

        self.object.answer_state = 2
        self.object.choosen_answer_obj=QuestionChoice.objects.get(
            pk=form.cleaned_data['choosen_answer']
            )
        self.object.save()
        return result

    def get_success_url(self):
        if self.object.wrd.block_mode == 1:
            self.block_questions = UserAnswer.objects.filter(wrd=self.object.wrd)
            try:
                self.next_question = self.block_questions.get(
                    block_number = self.object.block_number + 1
                    )
                return reverse('writing:writing', 
                            kwargs={'pk': self.next_question.pk})
            except ObjectDoesNotExist:
                return reverse('home')
        else:
            return reverse('writing:reviewing', kwargs={'pk': self.object.pk})

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
        writingform = WritingForm(self.object.answer_to,
                                      initial={
                        'choosen_answer': self.object.choosen_answer_obj.pk
                         })
        writingform.fields['choosen_answer'].widget.attrs.update(
                            {"onclick":"return false;"})
        context['form'] = writingform
        print('correct', self.object.answer_to.correct_choice.choice_text)
        context['correct_answer'] = self.object.answer_to.correct_choice.choice_text
        context['next_question_url'] = self.get_success_url()
        return context

    def get_success_url(self):
        self.wrd = self.object.wrd
        self.block_questions = UserAnswer.objects.filter(wrd=self.wrd)
        try:
            self.next_question = self.block_questions.get(
                block_number = self.object.block_number + 1
                )
        except ObjectDoesNotExist:
            return reverse('home')
        if self.wrd.finished:
            return reverse('writing:reviewing', 
                        kwargs={'pk': self.next_question.pk})
        else:
            return reverse('writing:writing', 
                        kwargs={'pk': self.next_question.pk})




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
