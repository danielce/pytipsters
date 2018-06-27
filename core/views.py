from django.shortcuts import render
from django.views.generic import UpdateView, ListView

from .forms import MatchTipFormSet, MatchTipForm
from .models import MatchTip, Match

# Create your views here.


class MatchListView(ListView):
    model = Match
    form_class = MatchTipForm
    queryset = Match.objects.all()
    template_name = 'core/match_list.html'
    context_object_name = 'fixtures'

    def get_context_data(self, **kwargs):
        data = super(MatchListView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['matchtips'] = MatchTipFormSet(self.request.POST)
        else:
            matchtips = MatchTip.objects.filter(user=self.request.user, pk__lt=4)
            data['matchtips'] = MatchTipFormSet(queryset=matchtips)
        return data
