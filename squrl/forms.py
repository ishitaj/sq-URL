from django import forms

class SqurlForm(forms.Form):
    """
    Squrl form for index page
    """
    target = forms.URLField(label='URL to shorten ')
    squrl = forms.CharField(label='Preferred squeezed URL ', required=False, max_length=50, min_length=4)
