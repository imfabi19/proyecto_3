from django.db import models

# Create your models here.
#  ------------------------ Clases ----------------------------

class Responsable (models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField( max_length=100)
    correo = models.EmailField()
    rut = models.CharField(max_length=12, unique= True )


    class Meta:
        verbose_name_plural = 'Responsables',
        ordering = ['nombre']
    def __str__(self):
        return f'{self.nombre}, {self.correo}'

#----------------------------Mascotas ----------------------------------

class Mascota (models.Model):
    nombre = models.CharField( max_length=100)
    año_nacimiento = models.IntegerField()
    especie = models.CharField( max_length=100, unique= True )
    responsable = models.ForeignKey(
        Responsable, on_delete=models.CASCADE, related_name='mascotas' )

    class Meta:
        verbose_name_plural = 'Mascotas'
        ordering = ['nombre']

    def __str__(self):
        return f'{self.nombre}, {self.año_nacimiento}'
