from django import forms
from .models import StaffProfile, LeaveRequest
from django.contrib.auth.models import User

class StaffProfileForm(forms.ModelForm):
    first_name = forms.CharField(label="First Name", max_length=30, required=False,
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name  = forms.CharField(label="Last Name",  max_length=30, required=False,
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model  = StaffProfile
        fields = ['department', 'phone', 'photo']          # profile fields
        widgets = {
            'department': forms.TextInput(attrs={'class': 'form-control'}),
            'phone':      forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')          # pop user instance
        super().__init__(*args, **kwargs)
        # initial values from User
        self.fields['first_name'].initial = self.user.first_name
        self.fields['last_name'].initial  = self.user.last_name

    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            profile.save()
            # save name back to User
            self.user.first_name = self.cleaned_data['first_name']
            self.user.last_name  = self.cleaned_data['last_name']
            self.user.save()
        return profile

class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model  = LeaveRequest
        fields = ['start_date', 'end_date', 'reason']
        widgets = {
            'start_date': forms.DateInput(attrs={'type':'date'}),
            'end_date':   forms.DateInput(attrs={'type':'date'}),
        }
