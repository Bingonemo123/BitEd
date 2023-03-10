from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms
from django.urls import reverse
from django.views.generic import FormView
from django.views.generic.detail import SingleObjectMixin
from django.http import HttpResponseForbidden


from home_page_tiles.models import HomePageTile
from .models import WriteRequestData
from .models import BLOCK_MODE_CHOICES
from .models import BLOCK_SECTOR_CHOICES
from questions.models import Question
from testwriting.models import UserAnswer

from django.core.exceptions import ValidationError
import random
# Create your views here.

def get_random_questions(qs, n):
    avail_ids = list(qs.values_list('id', flat=True))

    while True:
        try:
            pkl = random.sample(avail_ids, n) # change to range
        except ValueError:
            return None
        tile_return_list = []
        for pk in pkl:
            tile = qs.filter(pk=pk).first()
            if tile:
                tile_return_list.append(tile)
            else:
                break
        return tile_return_list


class writeRequestDataForm(forms.Form):
    block_mode = forms.ChoiceField(choices=BLOCK_MODE_CHOICES)
    block_total_questions = forms.IntegerField(initial=40)
    sector = forms.ChoiceField(choices=BLOCK_SECTOR_CHOICES)
    timed = forms.BooleanField(required=False)

    def clean_block_total_questions(self):
        questions_query_set = Question.objects        
        self.random_questions = get_random_questions(questions_query_set, 
                                   self.cleaned_data['block_total_questions'])
        if self.random_questions is None:
            raise ValidationError('Not Enough Questions in Database', code='invalid')
        else:
            return self.cleaned_data['block_total_questions']


class TileDetailView(DetailView):
    model = HomePageTile
    template_name = 'tiles/tile_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = writeRequestDataForm()
        return context


class writeRequestDataFormView(LoginRequiredMixin, SingleObjectMixin, FormView):
    template_name = 'tiles/tile_view.html'
    form_class = writeRequestDataForm
    model = HomePageTile
    login_url = '/dj_auth/login/'

    # from Formview how to pass data to form ? widget
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        
        self.wrd = WriteRequestData(
            requested_by = self.request.user,
            block_mode = form.cleaned_data['block_mode'],
            block_total_questions = form.cleaned_data['block_total_questions'],
            timed = form.cleaned_data['timed'],
            block_sector = form.cleaned_data['sector'],
            tile_created_from = self.object
        )
        self.wrd.save()

        # Generate New Block
        for blk_indx, question in enumerate(form.random_questions):
            userasnwer = UserAnswer(
                wrd=self.wrd,
                answer_to=question,
                block_number=blk_indx
            )
            userasnwer.save()

            if blk_indx == 0:
                self.first_question = userasnwer

        result =  super().form_valid(form)

        return result

    def get_success_url(self):
        return reverse('testwriting:testWriting_view', 
                       kwargs={'pk': self.first_question.pk})
        


class TileView(View):

    def get(self, request, *args, **kwargs):
        view = TileDetailView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = writeRequestDataFormView.as_view()
        return view(request, *args, **kwargs)
