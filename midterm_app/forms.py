from django import forms
from .models import Host, Discovery, PlanetarySystem, Planet

class HostForm(forms.ModelForm):
    class Meta:
        model = Host
        fields = '__all__'

class DiscoveryForm(forms.ModelForm):
    class Meta:
        model = Discovery
        fields = '__all__'

class PlanetarySystemForm(forms.ModelForm):
    class Meta:
        model = PlanetarySystem
        fields = '__all__'

class PlanetForm(forms.ModelForm):
    class Meta:
        model = Planet
        fields = '__all__'
