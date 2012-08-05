from django import forms

BC_CHOICES = ((0, '0'),
             (1, '1'),
             (2, '2'),
             (3, '3'),
             (4, '4'))

class BullsCowsForm(forms.Form):
    bulls = forms.ChoiceField(choices=BC_CHOICES)
    cows = forms.ChoiceField(choices=BC_CHOICES)