from django import forms

from .models import Tip


class TipForm(forms.ModelForm):
    class Meta:
        model = Tip
        fields = ['home_goals', 'away_goals']


TipFormSet = forms.modelformset_factory(
    Tip,
    fields=('home_goals', 'away_goals')
)
