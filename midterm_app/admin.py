from django.contrib import admin
from .models import Host, Discovery, Planet, SystemParameterReference, PlanetarySystem

class PlanetAdmin(admin.ModelAdmin):
    list_display = ('name', 'host_name', 'system_parameters')

    def host_name(self, obj):
        return obj.host.name
    host_name.short_description = 'Host Name'

    def system_parameters(self, obj):
        return obj.host.system.parameter_reference.name
    system_parameters.short_description = 'System Parameters'

admin.site.register(Host)
admin.site.register(Discovery)
admin.site.register(Planet, PlanetAdmin)
admin.site.register(SystemParameterReference)
admin.site.register(PlanetarySystem)
