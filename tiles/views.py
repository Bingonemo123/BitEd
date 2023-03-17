from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import SingleObjectMixin
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy

from tiles.models import Tile
from tiles.models import WriteRequestData
from writing.models import UserAnswer

from tiles.forms import writeRequestDataForm
from tiles.forms import TileCreateForm

# Create your views here.
class TileDetailView(DetailView):
    '''For Viewing Single Tiles Details'''
    model = Tile
    template_name = 'tiles/tile_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = writeRequestDataForm()
        return context


class writeRequestDataFormView(LoginRequiredMixin, SingleObjectMixin, FormView):
    '''For Submiting WRD'''
    template_name = 'tiles/tile_view.html'
    form_class = writeRequestDataForm
    model = Tile

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
        return reverse_lazy('writing:writing', 
                       kwargs={'pk': self.first_question.pk})
        


class TileView(View):

    def get(self, request, *args, **kwargs):
        view = TileDetailView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = writeRequestDataFormView.as_view()
        return view(request, *args, **kwargs)

class TileCreateView(LoginRequiredMixin, CreateView):
    model = Tile
    form_class = TileCreateForm
    template_name = 'tiles/tile_create.html'

    def get_success_url(self) -> str:
        return reverse_lazy('user_update', kwargs={'pk':self.request.user.pk})
    
    def form_valid(self, form):
        tile_obj = form.save(commit=False)
        tile_obj.author = self.request.user
        tile_obj.save()
        for parent_tile in form.cleaned_data['parents']:
            parent_tile.children.add(tile_obj)
            parent_tile.save()
        return super().form_valid(form)

