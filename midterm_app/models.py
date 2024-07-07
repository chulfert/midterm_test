from django.db import models
from django.utils.html import strip_tags
from bs4 import BeautifulSoup

class Host(models.Model):
    name = models.CharField(max_length=255)  # Host Name
    spectral_type = models.CharField(max_length=255)  # Spectral Type
    effective_temperature = models.FloatField(null=True, blank=True)  # Stellar Effective Temperature [K]
    radius = models.FloatField(null=True, blank=True)  # Stellar Radius [Solar Radius]
    mass = models.FloatField(null=True, blank=True)  # Stellar Mass [Solar Mass]
    metallicity = models.FloatField(null=True, blank=True)  # Stellar Metallicity [dex]
    metallicity_ratio = models.CharField(max_length=255, null=True, blank=True)  # Stellar Metallicity Ratio
    surface_gravity = models.FloatField(null=True, blank=True)  # Stellar Surface Gravity [log10(cm/s**2)]
    distance = models.FloatField(null=True, blank=True)  # Distance [pc]
    v_magnitude = models.FloatField(null=True, blank=True)  # V (Johnson) Magnitude
    k_magnitude = models.FloatField(null=True, blank=True)  # Ks (2MASS) Magnitude
    gaia_magnitude = models.FloatField(null=True, blank=True)  # Gaia Magnitude

    def __str__(self):
        return self.name

class SystemParameterReference(models.Model):
    name = models.CharField(max_length=255)  # System Parameter Reference
    right_ascension = models.CharField(max_length=255)  # RA [sexagesimal]
    ra_degrees = models.FloatField(null=True, blank=True)  # RA [deg]
    declination = models.CharField(max_length=255)  # Dec [sexagesimal]
    dec_degrees = models.FloatField(null=True, blank=True)  # Dec [deg]
    row_update = models.DateField(null=True, blank=True)  # Date of Last Update
    planet_publication_date = models.DateField(null=True, blank=True)  # Planetary Parameter Reference Publication Date
    release_date = models.DateField(null=True, blank=True)  # Release Date

    def __str__(self):
        return self.name
    
    def get_reference_link(self):
        soup = BeautifulSoup(self.name, "html.parser")
        link = soup.find('a')
        if link:
            return link.get('href'), link.text
        return None, self.name

class Discovery(models.Model):
    method = models.CharField(max_length=255)  # Discovery Method
    year = models.IntegerField(null=True, blank=True)  # Discovery Year
    reference_name = models.CharField(max_length=255)  # Discovery Reference
    facility = models.CharField(max_length=255)  # Discovery Facility
    telescope = models.CharField(max_length=255)  # Discovery Telescope

    def __str__(self):
        return f"{self.method} ({self.year})"

class PlanetarySystem(models.Model):
    host = models.OneToOneField(Host, on_delete=models.CASCADE, related_name='system')
    parameter_reference = models.ForeignKey(SystemParameterReference, on_delete=models.SET_NULL, null=True, related_name='systems')

    def __str__(self):
        return f"System of {self.host.name}"

class Planet(models.Model):
    name = models.CharField(max_length=255)  # Planet Name
    host = models.ForeignKey(Host, on_delete=models.CASCADE, related_name='planets')  # Host
    discovery = models.ForeignKey(Discovery, on_delete=models.CASCADE, related_name='planets')  # Discovery
    default_flag = models.BooleanField(default=False)  # Default Parameter Set
    controversial_flag = models.BooleanField(default=False)  # Controversial Flag
    parameter_reference = models.CharField(max_length=255, null=True, blank=True)  # Planetary Parameter Reference
    orbital_period = models.FloatField(null=True, blank=True)  # Orbital Period [days]
    semi_major_axis = models.FloatField(null=True, blank=True)  # Orbit Semi-Major Axis [au]
    radius = models.FloatField(null=True, blank=True)  # Planet Radius [Earth Radius]
    mass = models.FloatField(null=True, blank=True)  # Planet Mass [Earth Mass]
    mass_sin_i_earth = models.FloatField(null=True, blank=True)  # Planet Mass or Mass*sin(i) [Earth Mass]
    mass_sin_i_jupiter = models.FloatField(null=True, blank=True)  # Planet Mass or Mass*sin(i) [Jupiter Mass]
    mass_provenance = models.CharField(max_length=255, null=True, blank=True)  # Planet Mass or Mass*sin(i) Provenance
    eccentricity = models.FloatField(null=True, blank=True)  # Eccentricity
    insolation_flux = models.FloatField(null=True, blank=True)  # Insolation Flux [Earth Flux]
    equilibrium_temperature = models.FloatField(null=True, blank=True)  # Equilibrium Temperature [K]
    inclination = models.FloatField(null=True, blank=True)  # Inclination [deg]
    ttv_flag = models.BooleanField(default=False)  # Data show Transit Timing Variations
    transit_duration = models.FloatField(null=True, blank=True)  # Transit Duration [hours]

    def __str__(self):
        return self.name
