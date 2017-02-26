from django import forms
from datetime import date

from django_summernote.widgets import SummernoteInplaceWidget

from .models import Profile

class ProfileForm(forms.ModelForm):
    photo = forms.ImageField(label=('Thumbnail'),required=False,
                error_messages={'invalid':("Image files only")},
                widget=forms.FileInput)
    class Meta:
        model = Profile
        fields = ['photo', 'short_description', 'full_description',
                  'date_of_birth']
        widgets = {
        'short_description': forms.Textarea(attrs={'rows' : 2,
                                                   'style': 'resize:none;\
                                                             width:100%;',
                                                  }),
        'full_description' : SummernoteInplaceWidget(),
        'date_of_birth'    : forms.SelectDateWidget(
                             years=range(date.today().year - 5, 1910, -1)
                             ),
        }
