from typing import Optional
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, DetailView
from django.views.generic.edit import FormView
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse_lazy

from questions.forms import FolderSelectionForm
from questions.forms import basic_formset
from questions.forms import ChoiceFormset
from questions.forms import QuestionChoiceForm
from django.forms import modelformset_factory

from writing.forms import WritingForm
from django.contrib.auth.mixins import UserPassesTestMixin

from questions.forms import QuestionCreateForm
from questions.models import Question
from questions.models import QuestionChoice
from folder.models import Folder

# Create your views here.

class QuestionCreate(LoginRequiredMixin, CreateView):
    model = Question
    form_class = QuestionCreateForm
        
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
    
    def form_valid(self, form):
        self.formset = ChoiceFormset(self.request.POST)
        # Validate formsets
        if len(self.formset.non_form_errors()) != 0:
            return self.form_invalid(form)
        
        # Create Question 
        question_obj = form.save(commit=False)
        question_obj.owner = self.request.user
        question_obj.save()

        form.save_m2m()  # needed for taggit plugin

        correct_answer_setted = False

        for idx, choice in enumerate(self.formset):
            if choice.is_valid() and (choice.has_changed() or 
                                      choice.cleaned_data.get('choice_text')):
                choice_obj = choice.save(commit=False)
                if not correct_answer_setted:
                    question_obj.correct_choice = choice_obj    
                    correct_answer_setted = True 
                choice_obj.choice_to = question_obj
                choice_obj.save()

        return super().form_valid(form)
    
    def get_success_url(self) -> str:
        return reverse_lazy('select_folders', kwargs={"pk":self.object.pk})


class MyQuestionsUpdate(UpdateView):
    model = Question
    fields = ['question_title', 
              'question_body', 
              'question_explanation']
    
    # creating formset template based on QuestionChoice object with specific form
    # there is need of two kind of formsets. One is needed when question is displayed
    # for update, when is must be preloded with excisting questionchoice objects. Here we use
    # modelformset_facory since model in name.
    # second one is needed for recieving updates so cald freeform formset, where input is populated
    # form recived request. 

    basic_modelformset = modelformset_factory(QuestionChoice, 
                                         form=QuestionChoiceForm, extra=0)
        
    def form_valid(self, form):
        self.formset = ChoiceFormset(self.request.POST)

        # check if formset has any errors
        # forms inside formset aren't allowed to be empty. But inside formset forms don't rase form_invalide
        # errors. so when subformset form is empty it invalid but a.k.a formset is invalid, but non_form_errors
        # are none. (if of course there is not intrinsic formset error)
        if len(self.formset.non_form_errors()) != 0:
            return self.form_invalid(form)

        # delete all choices to recreate them
        QuestionChoice.objects.filter(choice_to=self.object).delete()
        correct_answer_setted = False

        for choice in self.formset:
            # print(choice.is_valid(), choice.cleaned_data)
            if choice.is_valid() and (choice.has_changed() or 
                                      choice.cleaned_data.get('choice_text')):
                choice_obj = choice.save(commit=False)
                if not correct_answer_setted:
                    self.object.correct_choice = choice_obj    
                    correct_answer_setted = True 
                choice_obj.choice_to = self.object
                choice_obj.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            if self.request.POST:
                # when there is post request, so formset was already populated
                # from database, there is no need form modelformser. In this case
                # it can be directly used 
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
    
    def get_success_url(self) -> str:
        return reverse_lazy('select_folders', kwargs={"pk":self.object.pk})
    
class QuestionPreview(UserPassesTestMixin, DetailView):
    model = Question
    template_name = "questions/question_preview.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = WritingForm(self.object)
        return context
    
    def test_func(self) :
        return self.request.user.is_superuser
    
class Selectfolders(FormView,  SingleObjectMixin):
    ''' For selecting folders after creating Question '''
    model = Question
    template_name = 'folder/folder_selection.html'
    form_class = FolderSelectionForm
    success_url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        print([f.name for f in Question._meta.get_fields()])
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        if not any([subfolders.get('is_selected', False) 
                for subfolders in form.cleaned_data]):
            root_folder = Folder.objects.filter(get='root')
            root_folder.questions.add(self.object)
            
        form.save()
        return super().form_valid(form)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        return kwargs


class SelectFolders(UpdateView):
    model = Question
    template_name = 'folder/folder_selection.html'
    success_url = reverse_lazy('my_questions')
    form_class = FolderSelectionForm
