from django.shortcuts import render
from rest_framework import viewsets
from .models import Responsable, Mascota
from .serializers import ResponsableSerializer, MascotaSerializer

class ResponsableViewSet(viewsets.ModelViewSet):
    queryset = Responsable.objects.all()
    serializer_class = ResponsableSerializer

class MascotaViewSet(viewsets.ModelViewSet):
    queryset = Mascota.objects.all()
    serializer_class = MascotaSerializer