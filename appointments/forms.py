from django import forms

from .models import RendezVous, Disponibilite


class PriseRendezVousForm(forms.Form):
    date = forms.DateField(label='Date', widget=forms.DateInput(attrs={'type': 'date'}))
    heure = forms.ChoiceField(label='Créneau horaire', choices=[])
    motif = forms.CharField(
        label='Motif de la consultation', required=False,
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Décrivez brièvement le motif (optionnel)'})
    )

    def __init__(self, *args, creneaux_disponibles=None, **kwargs):
        super().__init__(*args, **kwargs)
        creneaux_disponibles = creneaux_disponibles or []
        self.fields['heure'].choices = [(c.strftime('%H:%M'), c.strftime('%H:%M')) for c in creneaux_disponibles]


class DisponibiliteForm(forms.ModelForm):
    class Meta:
        model = Disponibilite
        fields = ['jour_semaine', 'heure_debut', 'heure_fin', 'duree_creneau_minutes']
        widgets = {
            'heure_debut': forms.TimeInput(attrs={'type': 'time'}),
            'heure_fin': forms.TimeInput(attrs={'type': 'time'}),
        }
