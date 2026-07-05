from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile


class InscriptionPatientForm(UserCreationForm):
    first_name = forms.CharField(label='Prénom', max_length=150, required=True)
    last_name = forms.CharField(label='Nom', max_length=150, required=True)
    email = forms.EmailField(label='Adresse e-mail', required=True)
    telephone = forms.CharField(label='Téléphone', max_length=20, required=False)
    date_naissance = forms.DateField(
        label='Date de naissance', required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            profile = user.profile
            profile.role = Profile.Role.PATIENT
            profile.telephone = self.cleaned_data.get('telephone', '')
            profile.date_naissance = self.cleaned_data.get('date_naissance')
            profile.save()
        return user


class InscriptionMedecinForm(UserCreationForm):
    first_name = forms.CharField(label='Prénom', max_length=150, required=True)
    last_name = forms.CharField(label='Nom', max_length=150, required=True)
    email = forms.EmailField(label='Adresse e-mail', required=True)
    telephone = forms.CharField(label='Téléphone', max_length=20, required=False)
    specialite = forms.CharField(label='Spécialité', max_length=100, required=True)
    numero_ordre = forms.CharField(label="Numéro d'ordre", max_length=50, required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            profile = user.profile
            profile.role = Profile.Role.MEDECIN
            profile.telephone = self.cleaned_data.get('telephone', '')
            profile.specialite = self.cleaned_data.get('specialite', '')
            profile.numero_ordre = self.cleaned_data.get('numero_ordre', '')
            profile.save()
        return user


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(label='Prénom', max_length=150)
    last_name = forms.CharField(label='Nom', max_length=150)
    email = forms.EmailField(label='E-mail')

    class Meta:
        model = Profile
        fields = [
            'telephone', 'date_naissance', 'adresse', 'photo',
            'specialite', 'biographie', 'tarif_consultation',
        ]
        widgets = {
            'date_naissance': forms.DateInput(attrs={'type': 'date'}),
            'biographie': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user_id:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
        if self.instance.role != Profile.Role.MEDECIN:
            del self.fields['specialite']
            del self.fields['biographie']
            del self.fields['tarif_consultation']

    def save(self, commit=True):
        profile = super().save(commit=False)
        profile.user.first_name = self.cleaned_data['first_name']
        profile.user.last_name = self.cleaned_data['last_name']
        profile.user.email = self.cleaned_data['email']
        if commit:
            profile.user.save()
            profile.save()
        return profile
