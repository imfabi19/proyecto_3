from django.test import TestCase

# Create your tests here.
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Mascota, Responsable


class ResponsableTests(APITestCase):
    def setUp(self):
        self.ana = Responsable.objects.create(
            nombre='Ana Pérez', correo='ana@ejemplo.cl', rut='11111111-1'
        )

    def test_crear_post(self):
        r = self.client.post('/responsable/crear', {
            'nombre': 'Juan Soto', 'correo': 'juan@ejemplo.cl', 'rut': '22222222-2'
        }, format='json')
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        self.assertEqual(r.data['correo'], 'juan@ejemplo.cl')
        self.assertIn('id', r.data)

    def test_crear_put(self):
        r = self.client.put('/responsable/crear', {
            'nombre': 'Juan Soto', 'correo': 'juan@ejemplo.cl', 'rut': '22222222-2'
        }, format='json')
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

    def test_crear_correo_repetido_400(self):
        r = self.client.post('/responsable/crear', {
            'nombre': 'Otra Ana', 'correo': 'ana@ejemplo.cl', 'rut': '33333333-3'
        }, format='json')
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('correo', r.data)

    def test_crear_campo_faltante_400(self):
        r = self.client.post('/responsable/crear', {'nombre': 'Sin correo'}, format='json')
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_crear_campo_vacio_400(self):
        r = self.client.post('/responsable/crear', {
            'nombre': '', 'correo': 'x@ejemplo.cl', 'rut': '1-9'
        }, format='json')
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('nombre', r.data)

    def test_listar(self):
        r = self.client.get('/responsables')
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r.data), 1)

    def test_modificar_parcial(self):
        r = self.client.patch(f'/responsable/modificar/{self.ana.id}', {'rut': '99999999-9'}, format='json')
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data['rut'], '99999999-9')
        self.assertEqual(r.data['nombre'], 'Ana Pérez')  # lo demás no cambia

    def test_modificar_invalido_400(self):
        r = self.client.patch(f'/responsable/modificar/{self.ana.id}', {'correo': 'no-es-correo'}, format='json')
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_modificar_inexistente_404(self):
        r = self.client.patch('/responsable/modificar/9999', {'rut': '1-9'}, format='json')
        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)

    def test_eliminar_en_cascada(self):
        Mascota.objects.create(nombre='Luna', año_nacimiento=2021, especie='Gato', responsable=self.ana)
        r = self.client.delete(f'/responsable/eliminar/{self.ana.id}')
        self.assertEqual(r.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Mascota.objects.count(), 0)

    def test_eliminar_inexistente_404(self):
        r = self.client.delete('/responsable/eliminar/9999')
        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)

    def test_metodo_no_permitido_405(self):
        self.assertEqual(self.client.delete('/responsables').status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(self.client.get('/responsable/crear').status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class MascotaTests(APITestCase):
    def setUp(self):
        self.ana = Responsable.objects.create(
            nombre='Ana Pérez', correo='ana@ejemplo.cl', rut='11111111-1'
        )
        self.luna = Mascota.objects.create(
            nombre='Luna', año_nacimiento=2021, especie='Gato', responsable=self.ana
        )

    def datos(self, **cambios):
        base = {'nombre': 'Toby', 'año_nacimiento': 2019, 'especie': 'Perro', 'responsable': self.ana.id}
        base.update(cambios)
        return base

    def test_crear_post(self):
        r = self.client.post('/mascota/crear', self.datos(), format='json')
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        self.assertEqual(r.data['responsable'], self.ana.id)  # el front depende de este campo

    def test_crear_put(self):
        r = self.client.put('/mascota/crear', self.datos(), format='json')
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

    def test_crear_sin_especie_400(self):
        datos = self.datos()
        del datos['especie']
        r = self.client.post('/mascota/crear', datos, format='json')
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('especie', r.data)

    def test_crear_responsable_inexistente_400(self):
        r = self.client.post('/mascota/crear', self.datos(responsable=9999), format='json')
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('responsable', r.data)

    def test_crear_año_no_entero_400(self):
        r = self.client.post('/mascota/crear', self.datos(año_nacimiento='abc'), format='json')
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_listar(self):
        r = self.client.get('/mascotas')
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data[0]['responsable'], self.ana.id)

    def test_listar_delete_405(self):
        r = self.client.delete('/mascotas')
        self.assertEqual(r.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_modificar_parcial(self):
        r = self.client.patch(f'/mascota/modificar/{self.luna.id}', {'especie': 'Felino'}, format='json')
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data['especie'], 'Felino')
        self.assertEqual(r.data['nombre'], 'Luna')

    def test_modificar_responsable_inexistente_400(self):
        r = self.client.patch(f'/mascota/modificar/{self.luna.id}', {'responsable': 9999}, format='json')
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_modificar_inexistente_404(self):
        r = self.client.patch('/mascota/modificar/9999', {'especie': 'Gato'}, format='json')
        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)

    def test_eliminar(self):
        r = self.client.delete(f'/mascota/eliminar/{self.luna.id}')
        self.assertEqual(r.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Mascota.objects.filter(id=self.luna.id).exists())

    def test_eliminar_inexistente_404(self):
        r = self.client.delete('/mascota/eliminar/9999')
        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)