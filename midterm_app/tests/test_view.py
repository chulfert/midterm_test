from django.test import TestCase, Client
from django.urls import reverse
from ..models import Host, Discovery, Planet, PlanetarySystem, SystemParameterReference
from ..forms import HostForm, DiscoveryForm, PlanetarySystemForm, PlanetForm

class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        # Create some test data
        self.host = Host.objects.create(name="Test Host", distance=100)
        self.system_parameter_reference = SystemParameterReference.objects.create(
            name="Test Reference",
            right_ascension="00h 00m 00s",
            ra_degrees=0.0,
            declination="00° 00' 00\"",
            dec_degrees=0.0
        )
        self.planetary_system = PlanetarySystem.objects.create(
            host=self.host,
            parameter_reference=self.system_parameter_reference
        )
        self.discovery = Discovery.objects.create(
            method="Test Method",
            year=2020,
            reference_name="Test Reference",
            facility="Test Facility",
            telescope="Test Telescope"
        )
        self.planet = Planet.objects.create(
            name="Test Planet",
            mass=1.0,
            radius=1.0,
            host=self.host,
            discovery=self.discovery
        )

    def test_landing_page(self):
        response = self.client.get(reverse('landing-page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'midterm_app/landing.html')

    def test_home(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'midterm_app/home.html')
        self.assertIn('total_hosts', response.context)
        self.assertIn('total_planets', response.context)

    def test_host_list(self):
        response = self.client.get(reverse('host_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'midterm_app/host_list.html')
        self.assertIn('hosts', response.context)

    def test_host_detail(self):
        response = self.client.get(reverse('host_detail', args=[self.host.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'midterm_app/host_detail.html')
        self.assertIn('host', response.context)

    def test_planet_list(self):
        response = self.client.get(reverse('planet_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'midterm_app/planet_list.html')
        self.assertIn('planets', response.context)

    def test_planet_detail(self):
        response = self.client.get(reverse('planet_detail', args=[self.planet.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'midterm_app/planet_detail.html')
        self.assertIn('planet', response.context)

    def test_api_endpoints(self):
        response = self.client.get(reverse('api_endpoints'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'midterm_app/api.html')

    def test_planets_near_earth(self):
        response = self.client.get(reverse('planets_near_earth'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'midterm_app/planets_ne.html')
        self.assertIn('planets', response.context)

    def test_systems_visualization(self):
        response = self.client.get(reverse('systems_visualization'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'midterm_app/viz.html')
        self.assertIn('hosts', response.context)

    def test_report_host_get(self):
        response = self.client.get(reverse('report-host'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'midterm_app/report_hosts.html')
        self.assertIn('form', response.context)

    def test_report_host_post(self):
        response = self.client.post(reverse('report-host'), {
            'name': 'New Host',
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
        })
        self.assertEqual(response.status_code, 302)  # Should redirect after form submission
        self.assertTrue(Host.objects.filter(name='New Host').exists())

    def test_report_discovery_get(self):
        response = self.client.get(reverse('report-discovery'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'midterm_app/report_discovery.html')
        self.assertIn('form', response.context)

    def test_report_discovery_post(self):
        response = self.client.post(reverse('report-discovery'), {
            'method': 'New Method', 
            'year': 2021, 
            'reference_name': 'New Reference', 
            'facility': 'New Facility', 
            'telescope': 'New Telescope'
        })
        self.assertEqual(response.status_code, 302)  
        self.assertTrue(Discovery.objects.filter(method='New Method').exists())

    def test_report_planetary_system_get(self):
        response = self.client.get(reverse('report-planetary-system'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'midterm_app/report_planetary_system.html')
        self.assertIn('form', response.context)

    def test_report_planetary_system_post(self):
        response = self.client.post(reverse('report-planetary-system'), {
            'host': self.host.id, 
            'parameter_reference': self.system_parameter_reference.id
        })
        self.assertEqual(response.status_code, 200) 
        self.assertTrue(PlanetarySystem.objects.filter(host=self.host).exists())

    def test_report_planet_get(self):
        response = self.client.get(reverse('report-planet'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'midterm_app/report_planet.html')
        self.assertIn('form', response.context)

    def test_report_planet_post(self):
        response = self.client.post(reverse('report-planet'), {
            'name': 'New Planet', 
            'mass': 1.5, 
            'radius': 1.2, 
            'host': self.host.id, 
            'discovery': self.discovery.id
        })
        self.assertEqual(response.status_code, 302) 
        self.assertTrue(Planet.objects.filter(name='New Planet').exists())

    def test_report_index(self):
        response = self.client.get(reverse('report_index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'midterm_app/report_index.html')
