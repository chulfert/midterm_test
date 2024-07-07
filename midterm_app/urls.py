from django.urls import path
from .views import (
    landing_page, home, host_list, host_detail, planet_list, planet_detail, HostListCreate, HostDetail, 
    DiscoveryListCreate, DiscoveryDetail, 
    PlanetarySystemListCreate, PlanetarySystemDetail, 
    PlanetListCreate, PlanetDetail, 
    SystemParameterReferenceListCreate, SystemParameterReferenceDetail,
    PlanetsByDiscoveryMethod, PlanetsByDiscoveryYear, PlanetsByMinMass,
    HostsByMinPlanets, PlanetsByControversialFlag, PlanetarySystemsByMaxDistance, report_discovery, report_host, report_index, report_planet, report_planetary_system
)

from . import views

urlpatterns = [
    path('', landing_page, name='landing-page'),

    path('home/', home, name='home'),
    path('hosts/', host_list, name='host_list'),
    path('hosts/<int:pk>/', host_detail, name='host_detail'),
    path('planets/', planet_list, name='planet_list'),
    path('planets/<int:pk>/', planet_detail, name='planet_detail'),
    path('planets/near-earth/', views.planets_near_earth, name='planets_near_earth'),
    path('systems/visualization/', views.systems_visualization, name='systems_visualization'),
    path('api', views.api_endpoints, name='api_endpoints'),
    path('api/hosts/', HostListCreate.as_view(), name='host-list-create'),
    path('api/hosts/<int:pk>/', HostDetail.as_view(), name='host-detail'),
    path('api/discoveries/', DiscoveryListCreate.as_view(), name='discovery-list-create'),
    path('api/discoveries/<int:pk>/', DiscoveryDetail.as_view(), name='discovery-detail'),
    path('api/systems/', PlanetarySystemListCreate.as_view(), name='system-list-create'),
    path('api/systems/<int:pk>/', PlanetarySystemDetail.as_view(), name='system-detail'),
    path('api/planets/', PlanetListCreate.as_view(), name='planet-list-create'),
    path('api/planets/<int:pk>/', PlanetDetail.as_view(), name='planet-detail'),
    path('api/system-parameters/', SystemParameterReferenceListCreate.as_view(), name='system-parameter-list-create'),
    path('api/system-parameters/<int:pk>/', SystemParameterReferenceDetail.as_view(), name='system-parameter-detail'),
    path('api/planets/discovery-method/', PlanetsByDiscoveryMethod.as_view(), name='planets-by-discovery-method'),
    path('api/planets/discovery-year/', PlanetsByDiscoveryYear.as_view(), name='planets-by-discovery-year'),
    path('api/planets/min-mass/', PlanetsByMinMass.as_view(), name='planets-by-min-mass'),
    path('api/hosts/min-planets/', HostsByMinPlanets.as_view(), name='hosts-by-min-planets'),
    path('api/planets/controversial-flag/', PlanetsByControversialFlag.as_view(), name='planets-by-controversial-flag'),
    path('api/systems/max-distance/', PlanetarySystemsByMaxDistance.as_view(), name='systems-by-max-distance'),
    path('report_index/', report_index, name='report_index'),
    path('report/host/', report_host, name='report-host'),
    path('report/discovery/', report_discovery, name='report-discovery'),
    path('report/planetary-system/', report_planetary_system, name='report-planetary-system'),
    path('report/planet/', report_planet, name='report-planet'),
]