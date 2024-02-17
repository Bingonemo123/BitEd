import time
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import SingleObjectMixin
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy


from folder.models import Folder
from folder.models import WriteRequestData
from writing.models import UserAnswer

from folder.forms import writeRequestDataForm
from folder.forms import folderCreateForm
from folder.forms import PersonalQueryQuestionsForm
from folder.forms import InlineSubfoldersListFormSet

# from folders.loader import subquery_personal_filter_stats_loader
from folder.loader import nested_personal_filter_stats_loader
from folder.loader import personal_filters_by_questions


# Create your views here.
class folderDetailView(DetailView):
    '''For Viewing Single folders Details'''
    model = Folder
    template_name = 'folder/folder_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = writeRequestDataForm()
        context['inline_formset'] = InlineSubfoldersListFormSet(instance=self.object)
        context['personal_form'] = PersonalQueryQuestionsForm()
        self.object.get_total_questions_num  # function

        if self.request.user.is_authenticated:
            max_questions_queryset = self.object.get_all_questions()

            st = time.time()
            ordered_agr_numbers = nested_personal_filter_stats_loader(max_questions_queryset, 
                                                                        self.request.user)
            print(time.time() - st)
            ordered_agr_numbers[0] = self.object.get_total_questions_num - ordered_agr_numbers[0]
            context['personal_form_iterator'] = zip(context['personal_form']["personal_filter"], 
                                                     ordered_agr_numbers )        
        return context
    
class writeRequestDataFormView(LoginRequiredMixin, SingleObjectMixin, FormView):
    '''For Submiting WRD'''
    template_name = 'folder/folder_view.html'
    form_class = writeRequestDataForm
    model = Folder

    # from Formview how to pass data to form ? widget
    def get_context_data(self, **kwargs):
        """ This get context data is for Post Request aka after error
        Load. There is Idea [TODO:] to make on get context function """
        context =  super().get_context_data(**kwargs)
        context['inline_formset'] = InlineSubfoldersListFormSet(self.request.POST,
                                                              instance=self.object)
        context['personal_form'] = PersonalQueryQuestionsForm(self.request.POST)
        
        return context
    
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        self.formset = InlineSubfoldersListFormSet(self.request.POST, 
                                                 instance=self.object)
        self.personal_form = PersonalQueryQuestionsForm(self.request.POST)

        choosen_questions = self.object.questions.all()
        for subfolderform in self.formset.cleaned_data:
            if subfolderform.get('is_selected', False):
                choosen_questions |= subfolderform.get("id").get_all_questions()

        if not self.personal_form.is_valid():
            return self.form_invalid(self.personal_form)

        self.questions_queryset = personal_filters_by_questions(choosen_questions,
                                                               self.personal_form,
                                                               self.request.user)

        return super().post(request, *args, **kwargs)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['questions_queryset'] = self.questions_queryset
        return kwargs

    def form_valid(self, form):
        
        self.wrd = WriteRequestData(
            requested_by=self.request.user,
            block_mode=form.cleaned_data['block_mode'],
            block_total_questions=len(form.random_questions),
            timed=form.cleaned_data['timed'],
            block_sector=form.cleaned_data['sector'],
            folder_created_from=self.object
        )
        self.wrd.save()

        # Generate New Block
        for blk_indx, question in enumerate(form.random_questions, start=1):
            userasnwer = UserAnswer(
                wrd=self.wrd,
                answer_to=question,
                block_number=blk_indx
            )
            userasnwer.save()

            if blk_indx == 1:
                self.first_question = userasnwer

        result =  super().form_valid(form)

        return result

    def get_success_url(self):
        return reverse_lazy('writing:writing', 
                       kwargs={'pk': self.first_question.pk})
        

class folderView(View):

    def get(self, request, *args, **kwargs):
        view = folderDetailView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = writeRequestDataFormView.as_view()
        return view(request, *args, **kwargs)

class folderCreateView(LoginRequiredMixin, CreateView):
    '''Currently in Profile'''
    # https://github.com/codingjoe/django-select2
    model = Folder
    form_class = folderCreateForm
    template_name = 'folder/folder_create.html'

    def get_success_url(self) -> str:
        return reverse_lazy('user_update', kwargs={'pk':self.request.user.pk})
    
    def form_valid(self, form):
        folder_obj = form.save(commit=False)
        folder_obj.author = self.request.user
        folder_obj.save()
        return super().form_valid(form)


class MyfoldersListView (ListView):
    model = Folder

    def get_queryset(self):
        quesryset = super().get_queryset()
        return quesryset.filter(author=self.request.user)
