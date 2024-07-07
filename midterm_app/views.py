import json
from .forms import HostForm, DiscoveryForm, PlanetarySystemForm, PlanetForm
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import generics
from django_filters import rest_framework as filters

from .models import Host, Discovery, Planet, SystemParameterReference, PlanetarySystem
from .serializers import HostSerializer, DiscoverySerializer, PlanetSerializer, SystemParameterReferenceSerializer, PlanetarySystemSerializer

def landing_page(request):
    return render(request, 'midterm_app/landing.html')

def home(request):
    total_hosts = Host.objects.count()
    total_planets = Planet.objects.count()
    return render(request, 'midterm_app/home.html', {'total_hosts': total_hosts, 'total_planets': total_planets})

def host_list(request):
    hosts = Host.objects.all()
    return render(request, 'midterm_app/host_list.html', {'hosts': hosts})

def host_detail(request, pk):
    host = get_object_or_404(Host, pk=pk)
    return render(request, 'midterm_app/host_detail.html', {'host': host})

def planet_list(request):
    planets = Planet.objects.all()
    return render(request, 'midterm_app/planet_list.html', {'planets': planets})

def planet_detail(request, pk):
    planet = get_object_or_404(Planet, pk=pk)
    return render(request, 'midterm_app/planet_detail.html', {'planet': planet})

def api_endpoints(request):
    return render(request, 'midterm_app/api.html')

def planets_near_earth(request):
    distance = request.GET.get('distance', 100)  # Default distance is 100 parsecs
    min_mass = request.GET.get('min_mass', None)
    max_mass = request.GET.get('max_mass', None)
    min_radius = request.GET.get('min_radius', None)
    max_radius = request.GET.get('max_radius', None)
    min_temp = request.GET.get('min_temp', None)
    max_temp = request.GET.get('max_temp', None)

    planets = Planet.objects.filter(host__distance__lte=distance)

    if min_mass:
        planets = planets.filter(mass__gte=min_mass)
    if max_mass:
        planets = planets.filter(mass__lte=max_mass)
    if min_radius:
        planets = planets.filter(radius__gte=min_radius)
    if max_radius:
        planets = planets.filter(radius__lte=max_radius)
    if min_temp:
        planets = planets.filter(equilibrium_temperature__gte=min_temp)
    if max_temp:
        planets = planets.filter(equilibrium_temperature__lte=max_temp)

    context = {
        'planets': planets,
        'distance': distance,
        'min_mass': min_mass,
        'max_mass': max_mass,
        'min_radius': min_radius,
        'max_radius': max_radius,
        'min_temp': min_temp,
        'max_temp': max_temp,
    }
    return render(request, 'midterm_app/planets_ne.html', context)

def systems_visualization(request):
    #hosts = Host.objects.filter(distance__lte=600)
    hosts = Host.objects.all()
    hosts_data = []

    for host in hosts:
        try:
            system = host.system
            if system and system.parameter_reference:
                ra_degrees = system.parameter_reference.ra_degrees
                dec_degrees = system.parameter_reference.dec_degrees
            else:
                continue
        except PlanetarySystem.DoesNotExist:
            ra_degrees = 0
            dec_degrees = 0
        if host.distance is None or 0: continue
        hosts_data.append({
            'id': host.id,
            'name': host.name,
            'distance': host.distance if host.distance is not None else 0,
            'ra': ra_degrees if ra_degrees is not None else 0,
            'dec': dec_degrees if dec_degrees is not None else 0,
        })

    hosts_json = json.dumps(hosts_data)
    return render(request, 'midterm_app/viz.html', {'hosts': hosts_json})


class HostListCreate(generics.ListCreateAPIView):
    queryset = Host.objects.all()
    serializer_class = HostSerializer

class DiscoveryListCreate(generics.ListCreateAPIView):
    queryset = Discovery.objects.all()
    serializer_class = DiscoverySerializer

class SystemParameterReferenceListCreate(generics.ListCreateAPIView):
    queryset = SystemParameterReference.objects.all()
    serializer_class = SystemParameterReferenceSerializer

class PlanetarySystemListCreate(generics.ListCreateAPIView):
    queryset = PlanetarySystem.objects.all()
    serializer_class = PlanetarySystemSerializer

class PlanetListCreate(generics.ListCreateAPIView):
    queryset = Planet.objects.all()
    serializer_class = PlanetSerializer

class HostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Host.objects.all()
    serializer_class = HostSerializer

class DiscoveryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Discovery.objects.all()
    serializer_class = DiscoverySerializer

class SystemParameterReferenceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SystemParameterReference.objects.all()
    serializer_class = SystemParameterReferenceSerializer

class PlanetarySystemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = PlanetarySystem.objects.all()
    serializer_class = PlanetarySystemSerializer

class PlanetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Planet.objects.all()
    serializer_class = PlanetSerializer

class PlanetFilter(filters.FilterSet):
    discovery_method = filters.CharFilter(field_name='discovery__method')

    class Meta:
        model = Planet
        fields = ['discovery_method']

class PlanetsByDiscoveryMethod(generics.ListAPIView):
    queryset = Planet.objects.all()
    serializer_class = PlanetSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = PlanetFilter

class PlanetFilterByYear(filters.FilterSet):
    discovery_year = filters.NumberFilter(field_name='discovery__year')

    class Meta:
        model = Planet
        fields = ['discovery_year']

class PlanetsByDiscoveryYear(generics.ListAPIView):
    queryset = Planet.objects.all()
    serializer_class = PlanetSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = PlanetFilterByYear

class PlanetFilterByMass(filters.FilterSet):
    min_mass = filters.NumberFilter(field_name='mass', lookup_expr='gt')

    class Meta:
        model = Planet
        fields = ['min_mass']

class PlanetsByMinMass(generics.ListAPIView):
    queryset = Planet.objects.all()
    serializer_class = PlanetSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = PlanetFilterByMass

class PlanetFilterByMass(filters.FilterSet):
    min_mass = filters.NumberFilter(field_name='mass', lookup_expr='gt')

    class Meta:
        model = Planet
        fields = ['min_mass']

class PlanetsByMinMass(generics.ListAPIView):
    queryset = Planet.objects.all()
    serializer_class = PlanetSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = PlanetFilterByMass

from django.db.models import Count

class HostsByMinPlanets(generics.ListAPIView):
    queryset = Host.objects.annotate(num_planets=Count('planets')).filter(num_planets__gt=1)
    serializer_class = HostSerializer

    def get_queryset(self):
        min_planets = self.request.query_params.get('min_planets', None)
        if min_planets is not None:
            self.queryset = self.queryset.filter(num_planets__gt=min_planets)
        return self.queryset

class PlanetFilterByControversialFlag(filters.FilterSet):
    controversial_flag = filters.BooleanFilter(field_name='controversial_flag')

    class Meta:
        model = Planet
        fields = ['controversial_flag']

class PlanetsByControversialFlag(generics.ListAPIView):
    queryset = Planet.objects.all()
    serializer_class = PlanetSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = PlanetFilterByControversialFlag

class PlanetFilterByControversialFlag(filters.FilterSet):
    controversial_flag = filters.BooleanFilter(field_name='controversial_flag')

    class Meta:
        model = Planet
        fields = ['controversial_flag']

class PlanetsByControversialFlag(generics.ListAPIView):
    queryset = Planet.objects.all()
    serializer_class = PlanetSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = PlanetFilterByControversialFlag

class PlanetarySystemFilterByDistance(filters.FilterSet):
    max_distance = filters.NumberFilter(field_name='host__distance', lookup_expr='lt')

    class Meta:
        model = PlanetarySystem
        fields = ['max_distance']

class PlanetarySystemsByMaxDistance(generics.ListAPIView):
    queryset = PlanetarySystem.objects.all()
    serializer_class = PlanetarySystemSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = PlanetarySystemFilterByDistance


def report_index(request):
    return render(request, 'midterm_app/report_index.html')

def report_host(request):
    if request.method == 'POST':
        form = HostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('host-list-create')  # Redirect to the list view after saving
    else:
        form = HostForm()
    return render(request, 'midterm_app/report_hosts.html', {'form': form})

def report_discovery(request):
    if request.method == 'POST':
        form = DiscoveryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('discovery-list-create')  # Redirect to the list view after saving
    else:
        form = DiscoveryForm()
    return render(request, 'midterm_app/report_discovery.html', {'form': form})

def report_planetary_system(request):
    if request.method == 'POST':
        form = PlanetarySystemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('system-list-create')  # Redirect to the list view after saving
    else:
        form = PlanetarySystemForm()
    return render(request, 'midterm_app/report_planetary_system.html', {'form': form})

def report_planet(request):
    if request.method == 'POST':
        form = PlanetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('planet-list-create')  # Redirect to the list view after saving
    else:
        form = PlanetForm()
    return render(request, 'midterm_app/report_planet.html', {'form': form})