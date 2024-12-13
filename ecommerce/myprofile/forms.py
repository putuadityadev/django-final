from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'profile_picture', 
            'bio', 
            'phone_number', 
            'address', 
            'role', 
            'store_name', 
            'store_description'
        ]
    
    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        
        # Validasi jika role seller
        if role == 'seller':
            if not cleaned_data.get('store_name'):
                raise forms.ValidationError("Store name is required for sellers")
            if not cleaned_data.get('store_description'):
                raise forms.ValidationError("Store description is required for sellers")
        
        return cleaned_data