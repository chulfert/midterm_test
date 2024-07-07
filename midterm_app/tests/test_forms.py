# tests/test_forms.py
from django.test import TestCase
from midterm_app.forms import HostForm

class HostFormTest(TestCase):
    def test_valid_form(self):
        data = {
            'name': 'Test Host',
            'spectral_type': 'G',
            'effective_temperature': 5500,
            'radius': 1.0,
            'mass': 1.0,
            'metallicity': 0.0,
            'metallicity_ratio': '[Fe/H]',
            'surface_gravity': 4.44,
            'distance': 150,
            'v_magnitude': 4.83,
            'k_magnitude': 4.83,
            'gaia_magnitude': 4.83
        }
        form = HostForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = {
            'name': '',  # Name is required, so this should fail
            'distance': 150
        }
        form = HostForm(data=data)
        self.assertFalse(form.is_valid())
        print(form.errors)
        self.assertEqual(len(form.errors), 2)  

        self.assertIn('name', form.errors)
        self.assertIn('spectral_type', form.errors)  
