from django import forms
from .models import StaffProfile, LeaveRequest

class StaffProfileForm(forms.ModelForm):
    class Meta:
        model  = StaffProfile
        fields = ['department', 'phone', 'photo']

class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model  = LeaveRequest
        fields = ['start_date', 'end_date', 'reason']
        widgets = {
            'start_date': forms.DateInput(attrs={'type':'date'}),
            'end_date':   forms.DateInput(attrs={'type':'date'}),
        }
