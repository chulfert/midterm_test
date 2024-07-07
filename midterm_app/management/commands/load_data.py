import csv
from datetime import datetime
import re
from ...models import Host, Discovery, Planet, SystemParameterReference, PlanetarySystem
from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist

class Command(BaseCommand):
    help = 'Load data from csv file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file_path', type=str, help='The path to the csv file to load data from')

    def handle(self, *args, **kwargs):
        csv_file_path = kwargs['csv_file_path']
        load_data_from_csv(self, csv_file_path)

def parse_float(value, default=None):
    try:
        return float(value)
    except (ValueError, TypeError):
        return default

def parse_int(value, default=None):
    try:
        return int(value)
    except (ValueError, TypeError):
        return default

def parse_date(value, format='%Y-%m-%d', default=None):
    try:
        return datetime.strptime(value, format).date()
    except (ValueError, TypeError):
        return default

def load_data_from_csv(self, csv_file_path):
    with open(csv_file_path, 'r') as file:
        reader = csv.DictReader(file)

        for row in reader:
            host, _ = Host.objects.get_or_create(
                name=row.get('hostname'),
                spectral_type=row.get('st_spectype', ''),
                defaults={
                    'effective_temperature': parse_float(row.get('st_teff')),
                    'radius': parse_float(row.get('st_rad')),
                    'mass': parse_float(row.get('st_mass')),
                    'metallicity': parse_float(row.get('st_met')),
                    'metallicity_ratio': row.get('st_metratio', ''),
                    'surface_gravity': parse_float(row.get('st_logg')),
                    'distance': parse_float(row.get('sy_dist')),
                    'v_magnitude': parse_float(row.get('sy_vmag')),
                    'k_magnitude': parse_float(row.get('sy_kmag')),
                    'gaia_magnitude': parse_float(row.get('sy_gaiamag'))
                }
            )

            system_param_ref, _ = SystemParameterReference.objects.get_or_create(
                name=row.get('sy_refname', ''),
                right_ascension=row.get('rastr', ''),
                ra_degrees=parse_float(row.get('ra')),
                declination=row.get('decstr', ''),
                dec_degrees=parse_float(row.get('dec')),
                defaults={
                    'row_update': parse_date(row.get('rowupdate')),
                    'planet_publication_date': parse_date(row.get('pl_pubdate'), '%Y-%m'),
                    'release_date': parse_date(row.get('releasedate'))
                }
            )

            discovery, created = Discovery.objects.get_or_create(
                method=row.get('discoverymethod', ''),
                year=parse_int(row.get('disc_year')),
                reference_name=row.get('disc_refname', ''),
                defaults={
                    'facility': row.get('disc_facility', ''),
                    'telescope': row.get('disc_telescope', '')
                }
            )

            if not created:
                self.stdout.write(self.style.WARNING(f'Discovery already exists: {discovery}'))

            planetary_system, created = PlanetarySystem.objects.get_or_create(
                host=host,
                defaults={'parameter_reference': system_param_ref}
            )

            if not created:
                planetary_system.parameter_reference = system_param_ref
                planetary_system.save()

            Planet.objects.get_or_create(
                name=row.get('pl_name', ''),
                host=host,
                discovery=discovery,
                defaults={
                    'default_flag': bool(parse_int(row.get('default_flag', 0))),
                    'controversial_flag': bool(parse_int(row.get('pl_controv_flag', 0))),
                    'parameter_reference': row.get('pl_refname', ''),
                    'orbital_period': parse_float(row.get('pl_orbper')),
                    'semi_major_axis': parse_float(row.get('pl_orbsmax')),
                    'radius': parse_float(row.get('pl_rade')),
                    'mass': parse_float(row.get('pl_masse')),
                    'mass_sin_i_earth': parse_float(row.get('pl_bmasse')),
                    'mass_sin_i_jupiter': parse_float(row.get('pl_bmassj')),
                    'mass_provenance': row.get('pl_bmassprov', ''),
                    'eccentricity': parse_float(row.get('pl_orbeccen')),
                    'insolation_flux': parse_float(row.get('pl_insol')),
                    'equilibrium_temperature': parse_float(row.get('pl_eqt')),
                    'inclination': parse_float(row.get('pl_orbincl')),
                    'ttv_flag': bool(parse_int(row.get('ttv_flag', 0))),
                    'transit_duration': parse_float(row.get('pl_trandur'))
                }
            )

            self.stdout.write(self.style.SUCCESS(f'Successfully imported {row.get("pl_name", "Unknown")}'))
