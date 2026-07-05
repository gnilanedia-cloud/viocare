from django import forms

from .models import Prescription


class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['medicaments', 'instructions', 'valide_jusquau']
        widgets = {
            'medicaments': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': 'Ex: Paracétamol 500mg - 1 comprimé x3/jour pendant 5 jours'
            }),
            'instructions': forms.Textarea(attrs={'rows': 3}),
            'valide_jusquau': forms.DateInput(attrs={'type': 'date'}),
        }
