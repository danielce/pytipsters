from django.shortcuts import redirect
from django.views.generic import ListView

from .forms import TipFormSet, TipForm
from .models import Tip, Fixture

# Create your views here.


class TipListView(ListView):
    model = Fixture
    form_class = TipForm
    formset_class = TipFormSet
    template_name = 'core/fixtures.html'
    context_object_name = 'fixtures'

    def get_queryset(self):
        return Tip.objects.filter(user=self.request.user, pk__lt=4)

    def get_context_data(self, **kwargs):
        data = super(TipListView, self).get_context_data(**kwargs)
        tips = self.get_queryset()
        data['tips'] = TipFormSet(queryset=tips)
        return data

    def post(self, *args, **kwargs):
        qs = self.get_queryset()
        formset = TipFormSet(
            self.request.POST, queryset=qs)

        if formset.is_valid():
            formset.save()

            return redirect('fixtures')

        raise ValueError(formset.errors)
