from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from .models import CustomUser, Profile


class RegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'student@coeruniversity.ac.in'}))

    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        domain = settings.ALLOWED_EMAIL_DOMAIN
        if not email.endswith('@' + domain):
            raise forms.ValidationError(f'Only @{domain} emails are allowed.')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('An account with this email already exists.')
        return email


class LoginForm(forms.Form):
    email    = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        domain = settings.ALLOWED_EMAIL_DOMAIN
        if not email.endswith('@' + domain):
            raise forms.ValidationError(f'Only @{domain} emails are allowed.')
        return email


class ProfileForm(forms.ModelForm):
    class Meta:
        model  = Profile
        fields = ['full_name', 'department', 'year', 'bio', 'picture']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
        }
