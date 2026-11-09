from rest_framework import serializers

from .models import Mascota, Responsable


class ResponsableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Responsable
        fields = ['id', 'nombre', 'correo', 'rut']


class MascotaSerializer(serializers.ModelSerializer):
    # "responsable" se envía y se recibe como el id del responsable.
    # Si el id no existe, el serializer responde error de validación (400).
    class Meta:
        model = Mascota
        fields = ['id', 'nombre', 'año_nacimiento', 'especie', 'responsable']
