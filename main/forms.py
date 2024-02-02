from django import forms

from .models import Tred


class TredForm(forms.ModelForm):

    class Meta:
        model = Tred
        fields = ['title', 'content', 'image']
