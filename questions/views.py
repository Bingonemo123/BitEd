from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, DetailView
from django.views.generic.edit import FormView
from django.views.generic.detail import SingleObjectMixin

from .forms import SelectTagsFormset
from django.forms import ModelForm, formset_factory
from django.forms import modelformset_factory


from .models import Question
from .models import QuestionChoice
from home_page_tiles.models import HomePageTile

# Create your views here.
# TODO: fix formsets [custom validation 
# empty_permitted but validate min manually]

class QuestionChoiceForm(ModelForm):

    class Meta:
        model = QuestionChoice
        fields = ['choice_text',]

basic_formset = formset_factory(QuestionChoiceForm, min_num=2,
                                        validate_min=True, extra=0)

class ChoiceFormset(basic_formset):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = False

class QuestionCreate(LoginRequiredMixin, CreateView):
    model = Question
    login_url='/dj_auth/login/'

    fields = ['question_title', 
              'question_body', 
              'question_explanation']
    
    success_url = '/create/select_tags/'
    
    def form_valid(self, form):
        self.formset = ChoiceFormset(self.request.POST)
        # Validate formsets
        if len(self.formset.non_form_errors()) != 0:
            return self.form_invalid(form)
        
        # Create Question 
        question_obj = form.save(commit=False)
        question_obj.owner = self.request.user
        question_obj.save()

        correct_answer_setted = False

        for idx, choice in enumerate(self.formset):
            if choice.is_valid() and (choice.has_changed() or 
                                      choice.cleaned_data.get('choice_text')):
                choice_obj = choice.save(commit=False)
                if not correct_answer_setted:
                    question_obj.correct_choice = choice_obj    
                    correct_answer_setted = True 
                choice_obj.choice_to = question_obj
                choice_obj.choice_id = idx
                choice_obj.save()
            
        # Create Tile
        tile_obj = HomePageTile(
            tile_headline = form.cleaned_data['question_title'],
            author = self.request.user,
            type_of_tile_char='Q',
            expected_reward=0,
            total_questions=1,

        )
        tile_obj.save()
        tile_obj.questions.add(question_obj)

        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = basic_formset(self.request.POST,
                                               error_messages={
                                            'too_few_forms': " Please submit at least %(num)d choices."
                                               })
            context['non_form_errors'] = context['formset'].non_form_errors()
        else:
           context['formset'] = basic_formset
        return context
    
    def get_success_url(self):
        return self.success_url + str(self.object.pk)


class MyQuestionsUpdate(UpdateView):
    model = Question
    fields = ['question_title', 
              'question_body', 
              'question_explanation']
    
    success_url = '/'
    basic_modelformset = modelformset_factory(QuestionChoice, 
                                         form=QuestionChoiceForm, extra=0)
        
    def form_valid(self, form):
        self.formset = ChoiceFormset(self.request.POST)

        if len(self.formset.non_form_errors()) != 0:
            return self.form_invalid(form)

        # delete all choices to recreate them
        QuestionChoice.objects.filter(choice_to=self.object).delete()
        correct_answer_setted = False

        for idx, choice in enumerate(self.formset):
            print(choice.is_valid(), choice.cleaned_data)
            if choice.is_valid() and (choice.has_changed() or 
                                      choice.cleaned_data.get('choice_text')):
                choice_obj = choice.save(commit=False)
                if not correct_answer_setted:
                    self.object.correct_choice = choice_obj    
                    correct_answer_setted = True 
                choice_obj.choice_to = self.object
                choice_obj.choice_id = idx
                choice_obj.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            if self.request.POST:
                context['formset'] = ChoiceFormset(self.request.POST,
                                                error_messages={
                                                'too_few_forms': 
                                                " Please submit at least %(num)d choices."
                                                })
                context['non_form_errors'] = context['formset'].non_form_errors()
            else:
                getmodelformset = self.basic_modelformset(
                        queryset=QuestionChoice.objects.filter(choice_to=self.object))
                context['formset'] = getmodelformset
            return context
    

class SelectTags(FormView,  SingleObjectMixin):
    ''' For selecting Tags after creating Question '''
    model = Question
    template_name = 'home_page_tiles/homepagetile_list.html'
    form_class = SelectTagsFormset
    success_url = '/'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['form_kwargs'] = {'obj': self.object}
        return kwargs

