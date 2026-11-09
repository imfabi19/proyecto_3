from django.contrib import admin

from .models import Mascota, Responsable


@admin.register(Responsable)
class ResponsableAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'correo', 'rut')
    search_fields = ('nombre', 'correo', 'rut')


@admin.register(Mascota)
class MascotaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'año_nacimiento', 'especie', 'responsable')
    list_filter = ('especie',)
    search_fields = ('nombre',)
