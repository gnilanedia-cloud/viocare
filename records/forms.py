from django import forms

from .models import DossierMedical, DocumentMedical


class DossierMedicalForm(forms.ModelForm):
    class Meta:
        model = DossierMedical
        fields = [
            'groupe_sanguin', 'allergies', 'antecedents_medicaux',
            'traitements_en_cours', 'contact_urgence_nom', 'contact_urgence_telephone',
        ]
        widgets = {
            'allergies': forms.Textarea(attrs={'rows': 3}),
            'antecedents_medicaux': forms.Textarea(attrs={'rows': 4}),
            'traitements_en_cours': forms.Textarea(attrs={'rows': 3}),
        }


class DocumentMedicalForm(forms.ModelForm):
    class Meta:
        model = DocumentMedical
        fields = ['titre', 'fichier']
