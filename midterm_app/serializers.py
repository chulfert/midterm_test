from rest_framework import serializers
from .models import Host, Discovery, Planet, SystemParameterReference, PlanetarySystem

class HostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Host
        fields = '__all__'

class DiscoverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Discovery
        fields = '__all__'

class SystemParameterReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemParameterReference
        fields = '__all__'

class PlanetarySystemSerializer(serializers.ModelSerializer):
    host = HostSerializer()
    parameter_reference = SystemParameterReferenceSerializer()

    class Meta:
        model = PlanetarySystem
        fields = '__all__'

class PlanetSerializer(serializers.ModelSerializer):
    host = HostSerializer()
    discovery = DiscoverySerializer()

    class Meta:
        model = Planet
        fields = '__all__'