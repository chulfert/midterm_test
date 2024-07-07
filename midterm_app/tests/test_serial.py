# tests/test_serializers.py
from django.test import TestCase
from ..models import Host
from ..serializers import HostSerializer

class HostSerializerTest(TestCase):
    def setUp(self):
        self.host_attributes = {
            'name': "Test Host",
            'spectral_type': "G",
            'effective_temperature': 5500,
            'radius': 1.0,
            'mass': 1.0,
            'metallicity': 0.0,
            'metallicity_ratio': "[Fe/H]",
            'surface_gravity': 4.44,
            'distance': 150,
            'v_magnitude': 4.83,
            'k_magnitude': 4.83,
            'gaia_magnitude': 4.83
        }
        self.host = Host.objects.create(**self.host_attributes)
        self.serializer = HostSerializer(instance=self.host)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(['id', 'name', 'spectral_type', 'effective_temperature', 'radius', 'mass', 'metallicity', 'metallicity_ratio', 'surface_gravity', 'distance', 'v_magnitude', 'k_magnitude', 'gaia_magnitude']))

    def test_name_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['name'], self.host_attributes['name'])
