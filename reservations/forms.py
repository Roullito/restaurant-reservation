from django import forms
from .models import Reservation
from datetime import time

class ReservationAdminForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        time_slots = []
        for h in range(12, 15):
            for m in (0, 30):
                time_slots.append((time(h, m), f"{h:02d}:{m:02d}"))
        for h in range(19, 22):
            for m in (0, 30):
                time_slots.append((time(h, m), f"{h:02d}:{m:02d}"))

        self.fields['reservation_time'] = forms.ChoiceField(choices=time_slots)
