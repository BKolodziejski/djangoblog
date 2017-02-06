from django import forms
from datetime import date

from django_summernote.widgets import SummernoteWidget

from .models import Profile

class ProfileForm(forms.ModelForm):
    photo = forms.ImageField(label=('Thumbnail'),required=False,
                error_messages={'invalid':("Image files only")},
                widget=forms.FileInput)
    class Meta:
        model = Profile
        fields = ['photo', 'short_description', 'full_description',
                  'date_of_birth', 'signature']
        widgets = {
        'short_description': forms.Textarea(),
        'full_description' : SummernoteWidget(),
        'date_of_birth'    : forms.SelectDateWidget(
                             years=range(1910, date.today().year)
                             ),
        }
