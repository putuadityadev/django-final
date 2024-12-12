from django import forms
from .models import AppleTechNews

class AppleTechNewsForm(forms.ModelForm):
    class Meta:
        model = AppleTechNews
        fields = ['title', 'content', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Tittle '
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Tulis detail berita disini...',
                'rows': 5
            })
        }
    
    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) < 10:
            raise forms.ValidationError("Judul terlalu pendek")
        return title