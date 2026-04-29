from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'phone', 'address', 'role')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        # Remove any non-numeric characters for checking length
        digits = ''.join(filter(str.isdigit, phone))
        
        if len(digits) != 10:
            raise forms.ValidationError("Mobile number must be exactly 10 digits.")
            
        # Ensure it has +977 prefix
        if not phone.startswith('+977'):
            phone = f"+977-{digits}"
        else:
            # Reformat to +977-XXXXXXXXXX
            phone = f"+977-{digits}"
            
        return phone
