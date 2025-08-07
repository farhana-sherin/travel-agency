from django import forms
from travelers.models import *

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['travel_date', 'num_people','destination', 'customer']
        widgets = {
            'travel_date': forms.DateInput(attrs={'type': 'date'}),
            'num_people': forms.NumberInput(attrs={'min': 1}),
            'destination': forms.HiddenInput(),
            'customer': forms.HiddenInput(),
            

           
        }