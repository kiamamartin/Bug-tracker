from django import forms
from .models import Ticket
from django.contrib.auth.models import User
from teams.models import Profile

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'priority', 'assigned_to']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter 'assigned_to' to only show developers
        self.fields['assigned_to'].queryset = User.objects.filter(profile__role=Profile.Role.DEVELOPER)
        
        
class StatusUpdateForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['status']