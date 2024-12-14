from django import forms
from .models import AppleTechNews

class AppleTechNewsForm(forms.ModelForm):
    class Meta:
        model = AppleTechNews
        fields = ['title', 'content', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Enter news title'
            }),
            'content': forms.Textarea(attrs={
                'placeholder': 'Write the detail here...',
                'rows': 5
            })
        }
    
    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) < 10:
            raise forms.ValidationError("Title is too short")
        return title