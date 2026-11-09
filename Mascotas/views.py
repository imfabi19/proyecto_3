from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Mascota, Responsable
from .serializers import MascotaSerializer, ResponsableSerializer


# ---------------------------------------------------------------------------
# Responsable
# ---------------------------------------------------------------------------

@api_view(['POST', 'PUT'])
def crear_responsable(request):
    serializer = ResponsableSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def listar_responsable(request):
    responsables = Responsable.objects.all().order_by('id')
    serializer = ResponsableSerializer(responsables, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PATCH'])
def modificar_responsable(request, id):
    try:
        responsable = Responsable.objects.get(id=id)
    except Responsable.DoesNotExist:
        return Response({'detail': 'Responsable no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = ResponsableSerializer(responsable, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def eliminar_responsable(request, id):
    try:
        responsable = Responsable.objects.get(id=id)
    except Responsable.DoesNotExist:
        return Response({'detail': 'Responsable no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    # on_delete=CASCADE: también se eliminan sus mascotas
    responsable.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# ---------------------------------------------------------------------------
# Mascota
# ---------------------------------------------------------------------------

@api_view(['POST', 'PUT'])
def crear_mascota(request):
    serializer = MascotaSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def listar_mascotas(request):
    mascotas = Mascota.objects.all().order_by('id')
    serializer = MascotaSerializer(mascotas, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PATCH'])
def modificar_mascota(request, id):
    try:
        mascota = Mascota.objects.get(id=id)
    except Mascota.DoesNotExist:
        return Response({'detail': 'Mascota no encontrada.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = MascotaSerializer(mascota, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def eliminar_mascota(request, id):
    try:
        mascota = Mascota.objects.get(id=id)
    except Mascota.DoesNotExist:
        return Response({'detail': 'Mascota no encontrada.'}, status=status.HTTP_404_NOT_FOUND)

    mascota.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
