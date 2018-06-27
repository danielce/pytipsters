from django import forms

from .models import MatchTip, Match


class MatchTipForm(forms.ModelForm):
    class Meta:
        model = MatchTip
        fields = ['home_goals', 'away_goals']


MatchTipFormSet = forms.modelformset_factory(
    MatchTip,
    fields=('home_goals', 'away_goals')
)