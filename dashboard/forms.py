
from django import forms
from .models import CandidatePics

class ImageForm(forms.ModelForm):
    class Meta:
        model = CandidatePics
        fields = ('images','user')
